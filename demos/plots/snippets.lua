-- The board's curves, re-read on save. Both are functions of t, so they move.

--- wave
-- a slow travelling sine under a symmetric envelope
return function(x)
    return math.sin(2 * x - 0.9 * t.from_begin) * math.exp(-0.2 * x ^ 2)
end

--- pulse
-- a wave packet whose envelope drifts back and forth
return function(x)
    local c = 1.7 * math.sin(0.35 * t.from_begin)
    return math.sin(4 * x) * math.exp(-1.1 * (x - c) ^ 2)
end
