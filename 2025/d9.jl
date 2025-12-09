#!/usr/bin/env julia

import Base.:+
using Printf

function parse_f(io)
    pts = Tuple{Int,Int}[]
    for line in eachline(io)
        s = strip(line)
        isempty(s) && continue
        x, y = split(s, ",")
        push!(pts, (parse(Int, x), parse(Int, y)))
    end
    return pts
end

function build_polygon(tiles)
    # Compress the coordinates
    xs = sort(unique(x for (x, _) in tiles))
    ys = sort(unique(y for (_, y) in tiles))
    ix = Dict(x => i-1 for (i, x) in enumerate(xs))
    iy = Dict(y => i-1 for (i, y) in enumerate(ys))

    W = 2 * length(xs) + 1
    H = 2 * length(ys) + 1
    g = fill(0, H, W)

    X(x) = 2 * ix[x] + 2
    Y(y) = 2 * iy[y] + 2

	# Set the polygon boundary
    n = length(tiles)
    for i in 1:n
        x1, y1 = tiles[i]
        x2, y2 = tiles[i == n ? 1 : i + 1]
        cx1, cy1 = X(x1), Y(y1)
        cx2, cy2 = X(x2), Y(y2)
        dx = (cx2 > cx1) - (cx2 < cx1)
        dy = (cy2 > cy1) - (cy2 < cy1)
        g[cy1, cx1] = 1
        while cx1 != cx2 || cy1 != cy2
            cx1 += dx
            cy1 += dy
            g[cy1, cx1] = 1
        end
    end

    # Finding inside and set the floor
    q = [(1, 1)]; g[1, 1] = 2; front = 1
    while front <= length(q)
        y, x = q[front]
        front += 1
        for (dy, dx) in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ny, nx = y + dy, x + dx
            if 1 <= ny <= H && 1 <= nx <= W && g[ny, nx] == 0
                g[ny, nx] = 2
                push!(q, (ny, nx))
            end
        end
    end

    for y in 1:H
        for x in 1:W
            if g[y, x] == 0
                g[y, x] = 1
            end
        end
    end

    return g, ix, iy
end

function prefix_sum_2d(g)
    H, W = size(g)
    ps = zeros(Int, H + 1, W + 1)
    for y in 1:H
        row_sum = 0
        for x in 1:W
            if g[y, x] == 1
                row_sum += 1
            end
            ps[y + 1, x + 1] = ps[y, x + 1] + row_sum
        end
    end
    return ps
end

function part1(tiles)
    best = 0
    n = length(tiles)
    for i in 1:n
        x1, y1 = tiles[i]
        for j in i+1:n
            x2, y2 = tiles[j]
            a = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if a > best
                best = a
            end
        end
    end
    return best
end

function part2(tiles)
    g, ix, iy = build_polygon(tiles)
    ps = prefix_sum_2d(g)
    X(x) = 2 * ix[x] + 2
    Y(y) = 2 * iy[y] + 2
    best = 0
    n = length(tiles)

    for i in 1:n
        x1, y1 = tiles[i]
        c1x, c1y = X(x1), Y(y1)
        for j in i+1:n
            x2, y2 = tiles[j]
            c2x, c2y = X(x2), Y(y2)

            gx1, gx2 = sort((c1x, c2x))
            gy1, gy2 = sort((c1y, c2y))

            area_cells = (gx2 - gx1 + 1) * (gy2 - gy1 + 1)
            s = ps[gy2 + 1, gx2 + 1] - ps[gy1, gx2 + 1] - ps[gy2 + 1, gx1] + ps[gy1, gx1]
            if s != area_cells
                continue
            end

            a = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if a > best
                best = a
            end
        end
    end

    return best
end

function main()
    filename = ARGS[1]
    floor = open(filename) do f
        parse_f(f)
    end
    println("Part 1: ", part1(floor))
    println("Part 2: ", part2(floor))
end

# julia d9.jl ./input/d9.txt
main()
