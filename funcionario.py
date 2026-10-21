from flask import request, jsonify, render_template
from banco import conectar_banco

def registrar_rotas_funcionario(app):
    
    # Rota para renderizar a página HTML de Funcionários
    @app.route("/funcionario")
    def pagina_funcionario():
        return render_template("funcionario.html")

    # READ - Listar todos os funcionários (com o nome da empresa via JOIN)
    @app.route("/api/funcionario", methods=["GET"])
    def listar_funcionario():
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT f.id, f.nome, f.cargo, f.salario, f.id_empresa, e.nome AS empresa_nome
                FROM funcionario f
                INNER JOIN empresa e ON f.id_empresa = e.id
                ORDER BY f.id DESC
            """
            cursor.execute(sql)
            funcionario = cursor.fetchall()
            cursor.close()
            conexao.close()
            return jsonify(funcionario), 200
        except Exception as erro:
            print("Erro ao listar funcionários:", erro)
            return jsonify({"erro": "Erro ao buscar funcionários"}), 500

    # READ - Obter um único funcionário por ID
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["GET"])
    def obter_funcionario(id_funcionario):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT id, nome, cargo, salario, id_empresa 
                FROM funcionario 
                WHERE id = %s
            """
            cursor.execute(sql, (id_funcionario,))
            funcionario = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            if not funcionario:
                return jsonify({"erro": "Funcionário não encontrado"}), 404
                
            return jsonify(funcionario), 200
        except Exception as erro:
            print("Erro ao obter funcionário:", erro)
            return jsonify({"erro": "Erro interno no servidor"}), 500

    # CREATE - Cadastrar novo funcionário
    @app.route("/api/funcionario", methods=["POST"])
    def criar_funcionario():
        dados = request.get_json()
        nome = dados.get("nome")
        cargo = dados.get("cargo")
        salario = dados.get("salario")
        id_empresa = dados.get("id_empresa")

        if not nome or not cargo or salario is None or not id_empresa:
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = "INSERT INTO funcionario (nome, cargo, salario, id_empresa) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, cargo, salario, id_empresa))
            conexao.commit()
            novo_id = cursor.lastrowid
            cursor.close()
            conexao.close()

            return jsonify({"mensagem": "Funcionário cadastrado com sucesso!", "id": novo_id}), 201
        except Exception as erro:
            print("Erro ao cadastrar funcionário:", erro)
            return jsonify({"erro": "Erro ao cadastrar funcionário"}), 500

    # UPDATE - Atualizar funcionário
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["PUT"])
    def atualizar_funcionario(id_funcionario):
        dados = request.get_json()
        nome = dados.get("nome")
        cargo = dados.get("cargo")
        salario = dados.get("salario")
        id_empresa = dados.get("id_empresa")

        if not nome or not cargo or salario is None or not id_empresa:
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = """
                UPDATE funcionario 
                SET nome = %s, cargo = %s, salario = %s, id_empresa = %s 
                WHERE id = %s
            """
            cursor.execute(sql, (nome, cargo, salario, id_empresa, id_funcionario))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Funcionário não encontrado"}), 404

            return jsonify({"mensagem": "Funcionário atualizado com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao atualizar funcionário:", erro)
            return jsonify({"erro": "Erro ao atualizar funcionário"}), 500

    # DELETE - Remover funcionário
    @app.route("/api/funcionario/<int:id_funcionario>", methods=["DELETE"])
    def deletar_funcionario(id_funcionario):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM funcionario WHERE id = %s", (id_funcionario,))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Funcionário não encontrado"}), 404

            return jsonify({"mensagem": "Funcionário excluído com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao excluir funcionário:", erro)
            return jsonify({"erro": "Erro interno ao excluir funcionário"}), 500