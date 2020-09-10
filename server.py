from flask import Flask
from flask_restful import Resource, Api
from flask import request

app = Flask(__name__)
api = Api(app)

sala = 1
class velha():
	def __init__(self):
		self.jogo = [99 for i in range(9)]
		self.turn = 0
	def jogar(self,jogador,jogada):
		if self.turn == jogador and self.jogo[jogada-1] == 99:
			self.jogo[jogada-1] = jogador
			self.turn = 0 if jogador == 1 else 1
			return True
		return False
		
def verifica(jogo):
	if sum(jogo[0:3]) == 0 or sum(jogo[3:6]) == 0 or sum(jogo[6:]) == 0:
		return "Jogador O ganhou"
	if sum(jogo[0:3]) == 3 or sum(jogo[3:6]) == 3 or sum(jogo[6:]) == 3:
		return "Jogador X ganhou"
	if jogo[0]+jogo[3]+jogo[6] == 0 or jogo[1]+jogo[4]+jogo[7] == 0 or jogo[2]+jogo[5]+jogo[8] == 0:
		return "Jogador O ganhou"
	if jogo[0]+jogo[3]+jogo[6] == 3 or jogo[1]+jogo[4]+jogo[7] == 3 or jogo[2]+jogo[5]+jogo[8] == 3:
		return "Jogador X ganhou"
	if jogo[0]+jogo[4]+jogo[8] == 0 or jogo[2]+jogo[4]+jogo[6] == 0:
		return "jogador O ganhou"
	if jogo[0]+jogo[4]+jogo[8] == 3 or jogo[2]+jogo[4]+jogo[6] == 3:
		return "jogador X ganhou"
	for i in jogo:
		if i == 99:
			return "ainda"
	return "Velha"
		
clientes = [{'Num_jogadores':0,'Turn':0,'velha':velha(),'notificados':0} for i in range(1000)]

@app.route('/estado/<sala>', methods=['GET', 'POST'])
def estado(sala):
	global clientes
	jogo = clientes[int(sala)]['velha']
	value = verifica(jogo.jogo)
	if value != "ainda":
		if clientes[int(sala)]['notificados'] == 1:
			clientes[int(sala)] = {'Num_jogadores':0,'Turn':0,'velha':velha(),'notificados':0}
		else:
			clientes[int(sala)]['notificados'] += 1
	return {'estado':jogo.jogo,'atual':value}
    
@app.route('/inicial', methods=['GET', 'POST'])
def criar_sala():
    global sala,clientes
    return {'Sala':str(sala)}

@app.route('/entrar/<sala>', methods=['GET','POST'])
def entrar_sala(sala):
	global clientes
	if int(clientes[int(sala)]['Num_jogadores']) <= 1 :
		responde = {'sala':True, 'jogador':clientes[int(sala)]['Num_jogadores']}
		clientes[int(sala)]['Num_jogadores'] += 1
		return responde

@app.route('/jogada/<sala>/<jogador>/<jogada>', methods=['GET','POST'])
def jogada(sala,jogador,jogada):
	global clientes
	return {'situacao':clientes[int(sala)]['velha'].jogar(int(jogador),int(jogada))}

@app.route('/test/<uuid>', methods=['GET', 'POST'])
def parse_request(uuid):
    print(uuid)
    return {'send':'correct'}

@app.route('/up', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)

if __name__ == '__main__':
    app.run(port=8080,debug=True)
