from flask import request, jsonify, render_template
from banco import conectar_banco

def registrar_rotas_empresa(app):

    # Rota para renderizar a página HTML de empresa
    @app.route("/empresa")
    def pagina_empresa():
        return render_template("empresa.html")

    # READ - Listar todas as empresa
    @app.route("/api/empresa", methods=["GET"])
    def listar_empresa():
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, cnpj, cidade, ativo FROM empresa ORDER BY id DESC")
            empresa = cursor.fetchall()
            cursor.close()
            conexao.close()
            return jsonify(empresa), 200
        except Exception as erro:
            print("Erro ao listar empresa:", erro)
            return jsonify({"erro": "Erro ao buscar empresa"}), 500

    # READ - Obter uma empresa por ID
    @app.route("/api/empresa/<int:id_empresa>", methods=["GET"])
    def obter_empresa(id_empresa):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, cnpj, cidade, ativo FROM empresa WHERE id = %s", (id_empresa,))
            empresa = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            if not empresa:
                return jsonify({"erro": "Empresa não encontrada"}), 404
                
            return jsonify(empresa), 200
        except Exception as erro:
            print("Erro ao obter empresa:", erro)
            return jsonify({"erro": "Erro interno no servidor"}), 500

    # CREATE - Cadastrar nova empresa
    @app.route("/api/empresa", methods=["POST"])
    def criar_empresa():
        dados = request.get_json()
        nome = dados.get("nome")
        cnpj = dados.get("cnpj")
        cidade = dados.get("cidade")
        ativo = dados.get("ativo", 1)

        if not nome:
            return jsonify({"erro": "O nome da empresa é obrigatório!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = "INSERT INTO empresa (nome, cnpj, cidade, ativo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, cnpj, cidade, ativo))
            conexao.commit()
            novo_id = cursor.lastrowid
            cursor.close()
            conexao.close()

            return jsonify({"mensagem": "Empresa cadastrada com sucesso!", "id": novo_id}), 201
        except Exception as erro:
            print("Erro ao cadastrar empresa:", erro)
            return jsonify({"erro": "Erro ao cadastrar empresa"}), 500

    # UPDATE - Atualizar empresa existente
    @app.route("/api/empresa/<int:id_empresa>", methods=["PUT"])
    def atualizar_empresa(id_empresa):
        dados = request.get_json()
        nome = dados.get("nome")
        cnpj = dados.get("cnpj")
        cidade = dados.get("cidade")
        ativo = dados.get("ativo", 1)

        if not nome:
            return jsonify({"erro": "O nome da empresa é obrigatório!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = "UPDATE empresa SET nome = %s, cnpj = %s, cidade = %s, ativo = %s WHERE id = %s"
            cursor.execute(sql, (nome, cnpj, cidade, ativo, id_empresa))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Empresa não encontrada"}), 404

            return jsonify({"mensagem": "Empresa atualizada com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao atualizar empresa:", erro)
            return jsonify({"erro": "Erro ao atualizar empresa"}), 500

    # DELETE - Remover empresa
    @app.route("/api/empresa/<int:id_empresa>", methods=["DELETE"])
    def deletar_empresa(id_empresa):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM empresa WHERE id = %s", (id_empresa,))
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Empresa não encontrada"}), 404

            return jsonify({"mensagem": "Empresa excluída com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao excluir empresa:", erro)
            return jsonify({"erro": "Não foi possível excluir. Verifique se existem funcionários vinculados a esta empresa."}), 400