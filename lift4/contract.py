import islpy as isl

def to_sets(union_set):
    sets = []
    union_set.foreach_set(lambda x: sets.append(x))
    return sets


def to_maps(union_map):
    maps = []
    union_map.foreach_map(lambda x: maps.append(x))
    return maps


def rewrite_stmt(expr, stmt_map):
    if expr[0] == 'var':
        return ('var', stmt_map.apply_range(expr[1]))
    elif expr[0] == 'const':
        return expr
    elif expr[0] == 'call':
        return (expr[0],expr[1],tuple(rewrite_stmt(e,stmt_map) for e in expr[2]))
    else:
        raise NotImplementedError


def subst_stmt(expr, v, stmt_map, stmt, stmt_domain):
    if expr[0] == 'var':
        if expr[1].get_tuple_name(isl.dim_type.out) != v:
            return ('var',expr[1].intersect_domain(stmt_domain))

        return rewrite_stmt(stmt, stmt_map)
    elif expr[0] == 'const':
        return expr
    elif expr[0] == 'call':
        return (expr[0],expr[1],tuple(subst_stmt(e,v,stmt_map,stmt,stmt_domain) for e in expr[2]))
    else:
        raise NotImplementedError


def contract_single_use_def_arrays(ctx):
    def find_contractible():
        reduction_arrays = ctx.fini_stmts.get_assign_map().range()
        use_map = ctx.get_use_map()

        for k, v in ctx.intermediate_arrays.items():
            if not v.intersect(reduction_arrays).is_empty():
                continue

            uses = use_map.intersect_range(v)
            if not uses.is_injective():
                continue

            return k, uses

    while True:
        defined_by = ctx.def_stmts.get_assign_map().reverse()
        contractible = find_contractible()
        if contractible is None:
            return

        k, uses = contractible

        for domain in to_sets(uses.domain()):
            m, = to_maps(uses.intersect_domain(domain))
            maps = to_maps(m.apply_range(defined_by))

            for stmt_map in maps:
                assert not stmt_map.is_empty()

                stmt_domain = stmt_map.domain()
                name = stmt_domain.get_tuple_name()
                stmt = ctx.def_stmts.get(name, ctx.update_stmts.get(name, None))

                name2 = stmt_map.get_tuple_name(isl.dim_type.out)

                new_stmt = (
                    stmt[0].intersect_domain(stmt_domain),
                    subst_stmt(stmt[1], k, stmt_map, ctx.def_stmts[name2][1], stmt_domain))

                if name in ctx.def_stmts:
                    ctx.def_stmts.add(new_stmt)
                    ctx.def_stmts.subtract(stmt_domain)
                    ctx.def_stmts.subtract(stmt_map.range())
                elif name in ctx.update_stmts:
                    ctx.update_stmts.add(new_stmt)
                    ctx.update_stmts.subtract(stmt_domain)
                    ctx.def_stmts.subtract(stmt_map.range())
                else:
                    raise NotImplementedError

        del ctx.intermediate_arrays[k]


def contract_arrays(ctx):
    contract_single_use_def_arrays(ctx)
