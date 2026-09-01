import math

dump = []
dump.append(211286818345627549183608678726370412218029639873054513839005340650674982169404937862395980568550063504804783328450267566224937880641772833325018028629959635) 

with open("dump.txt", "r") as arquivo:
    dump.extend([int(linha) for linha in arquivo])

print(len(dump))

t_list = []
for i in range(6):
    t_list.append(dump[i+1] - dump[i])

kN_list = []

for i in range(4):
    aux = (t_list[i+2] * t_list[i]) - (t_list[i+1]**2)
    kN_list.append(aux)

n = math.gcd(*kN_list)
print(n)

M = (t_list[1] * pow(t_list[0], -1, n)) % n
print(f"O multiplicador M é: {M}")

C = (dump[1] - M * dump[0]) % n
print(f"O incremento C é: {C}")