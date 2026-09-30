N = int(input())

Event = []
for _ in range(N):
    Event.append(list(map(int,input().split())))

enable_flag = True
Potion_stack = [ [] for _ in range(N + 1)]

Important_event = []
for i in range(N):
    if Event[i][0] == 1:
        Potion_stack[Event[i][1]].append(i)
    else:
        if len(Potion_stack[Event[i][1]]) > 0:
            p = Potion_stack[Event[i][1]].pop()
            Important_event.append([1, p])
            Important_event.append([2, i])
        else:
            enable_flag = False

Important_event.sort(key=lambda x:x[1])
answer_state = []
get_potions = set()
for ty, time in Important_event:
    if ty == 1:
        get_potions.add(time)
for i in range(N):
    if Event[i][0] == 1:
        if i in get_potions:
            answer_state.append(1)
        else:
            answer_state.append(0)

if enable_flag:
    answer = 0
    now_potion = 0
    for ty, time in Important_event:
        if ty == 1:
            now_potion += 1
        else:
            now_potion -= 1
        answer = max(answer, now_potion)
    print(answer)
    print(*answer_state)
else:
    print(-1)