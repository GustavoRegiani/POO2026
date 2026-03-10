alunos = [''] * 5 
for i in range (0 , len('alunos') - 1):
    alunos[i]=input('fala o nome de um aluno:')

print('lista de alunos:')
for i in range(0, len('alunos')):
    print('Aluno', i+1 , alunos[i])