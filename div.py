function div(items,o)
  class Num:
    def __init__(i,inits=[]):
      i.mu, i.n=0, i.m2= 0,0,0
      map(i.add, inits)
    def add(i,x):
      i.n += 1
      delta = x - i.mu
      i.mu += delta/i.n
      i.m2 += delta*(x - i.mu)
    def sub(i,x):
      i.n   = max(0,i.n - 1)
      delta = x - i.mu
      i.mu  = max(0,i.mu - delta/i.n)
      i.m2  = max(0,i.m2 - delta*(x - i.mu))
    def sd(i):
      return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  class Sym(About):
    def __init__(i,inits=[]): 
      i.counts,i.n = {},0
    def add(i,x):
      i.n += 1
      new = i.counts[x] = i.counts.get(x,0) + 1

  o.tiny   = o.tiny   or sd(num0(collect(items,o.x))) * o.cohen
  o.enough = o.enough or (#items)^0.5
  local function xpect(l,r,n) return l.n/n*ent(l) + r.n/n*ent(r) end
  local function divide(items,out,lvl,cut)
    local xlhs, xrhs   = num0(), num0(collect(items,o.x))
    local ylhs, yrhs   = sym0(), sym0(collect(items,o.y))
    local score,score1 = ent(yrhs), nil
    local k0,e0,ke0    = ke(yrhs) 
    local reportx       = copy(xrhs)
    local reporty      = copy(yrhs)
    local n            = #items
    local start, stop  = o.x(first(items)), o.x(last(items))
    for i,new in pairs(items) do
      local x1 = o.x(new)
      local y1 = o.y(new)
      if x1 ~= IGNORE then
	num1( xlhs,x1); sym1( ylhs,y1)  -- the code giveth
	unnum(xrhs,x1); unsym(yrhs,y1)  -- the code taketh away
	if xrhs.n < o.enough then
	  break
	else
	  if xlhs.n >= o.enough then
	    if x1 - start > o.tiny then
	      if stop - x1 > o.tiny then
		if x1 < o.x(items[i+1])  then
		  local score1 = xpect(ylhs,yrhs,n)
		  if score1 * o.trivial < score then
		    local gain       = e0 - score1
		    local k1,e1, ke1 = ke(yrhs) -- k1,e1 not used
		    local k2,e2, ke2 = ke(ylhs) -- k2,e2 not used
		    local delta      = math.log(3^k0 - 2,2) - (ke0 - ke1 - ke2)
		    local border     = (math.log(n-1,2)  + delta) / n
		    if gain > border then
		      cut,score = i,score1 end end end end end end end end
			   end -- for loop
    if o.verbose then
      print(s5(n),nstr('|..',lvl)) end
    if cut then
      divide( sub(items,1,   cut), out, lvl+1)
      divide( sub(items,cut+1), out, lvl+1)
    else
      out[#out+1] = RANGE{label=o.label,score=score,x=reportx,y=reporty,
			  n=n, id=#out, lo=start, up=stop, _has=items}
    end
    return out
  end
  -----------------------------------
  
  local items1 = select(items, function(z) return o.x(z) ~= IGNORE end)
  table.sort(items1, function (z1,z2) return o.x(z1) < o.x(z2) end)
  return divide(items1, {}, 0)
end
