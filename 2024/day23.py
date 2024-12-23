def read_file(f):
    g={}
    for l in open(f):
        l=l.strip()
        if not l:continue
        a,b=l.split('-')
        if a not in g:g[a]=set()
        if b not in g:g[b]=set()
        g[a].add(b)
        g[b].add(a)
    return g

def find_triangles(g):
    t=set()
    n=sorted(g.keys())
    for i in range(len(n)):
        for j in range(i+1,len(n)):
            for k in range(j+1,len(n)):
                a,b,c=n[i],n[j],n[k]
                if b in g[a] and c in g[a] and b in g[c] and a in g[b] and c in g[b] and a in g[c]:
                    t.add((a,b,c))
    return t

def largest_set_search(R,P,X,g,m):
    if len(R)+len(P)<=len(m[0]):return
    if not P and not X:
        if len(R)>len(m[0]):m[0]=R.copy()
        return
    if P:u=next(iter(P))
    else:u=next(iter(X))
    for v in list(P-g[u]):
        r=R|{v}
        p=P&g[v]
        x=X&g[v]
        largest_set_search(r,p,x,g,m)
        P.remove(v)
        X.add(v)

def find_passwd(g):
    R=set()
    P=set(g.keys())
    X=set()
    m=[set()]
    largest_set_search(R,P,X,g,m)
    return sorted(m[0])

def main(file):
    g=read_file(file)
    tri=find_triangles(g)
    tri_t=[x for x in tri if any(y.startswith('t') for y in x)]
    print(f"Q1: {len(tri_t)} contain at least one computer with initial t")
    lan=find_passwd(g)
    print(f"Q2: The password is {(','.join(lan))}")

if __name__=="__main__":
    main('./inputs/day23_1.txt')