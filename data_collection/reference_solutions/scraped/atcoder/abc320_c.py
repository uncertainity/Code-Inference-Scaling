M=int(input())
S=[input().strip() for _ in range(3)]

INF=10**9
ans=INF

for d in range(10):
    pos=[[] for _ in range(3)]
    for i in range(3):
        for t in range(M):
            if S[i][t]==str(d):
                pos[i].append(t)

    if any(len(p)==0 for p in pos):
        continue

    for a in pos[0]:
        for b in pos[1]:
            for c in pos[2]:
                t0=a
                t1=b
                t2=c
                used=set()
                cur=0
                for t in [t0,t1,t2]:
                    while t in used:
                        t+=M
                    used.add(t)
                    cur=max(cur,t)
                ans=min(ans,cur)

print(ans if ans<INF else -1)
