def crearevento(bd, titulo, categoria_atividade, descricao, palestrante, data, horario, duracao, local,
                quantidade_vagas, info_complementar, token_evento, encerrado):
    id=bd.cursor.execute("INSERT INTO [dbo].[evento] ([titulo], [categoria_atividade], [descricao],"
                         "[palestrante], [data], [horario], [duracao], [local], [quantidade_vagas],"
                         "[info_complementares], [token_evento], [encerrado]) OUTPUT INSERTED.id VALUES"
                         "( '{}', ({}), '{}', '{}', '{}', '{}', '{}', '{}', '{}',"
                         " '{}', '{}', '{}')".format(titulo, categoria_atividade, descricao,
                                                     palestrante, data, horario, duracao, local,
                                                     quantidade_vagas, info_complementar,
                                                     token_evento, encerrado)).fetchone()
    bd.cursor.commit()
    id = str(id[0])
    token_evento = data + id

    bd.cursor.execute("UPDATE [dbo].[evento] SET [token_evento]={} WHERE [id]={}".format(token_evento, id))
    bd.cursor.commit()


def readevento(bd):
    dicio = []
    dic = bd.cursor.execute("SELECT * FROM [dbo].[evento] ORDER BY [evento].[data]").fetchall()
    for i in dic:
         dicio.append({
                "id": f"{i[0]}",
                "titulo": f"{i[1]}",
                "categoria_atividade": f"{i[2]}",
                "descricao": f"{i[3]}",
                "palestrante": f"{i[4]}",
                "data": f"{i[5]}",
                "horario": f"{i[6]}",
                "duracao": f"{i[7]}",
                "local": f"{i[8]}",
                "quantidade_vagas": f"{i[9]}",
                "info_complementar": f"{i[10]}",
                "token_evento": f"{i[11]}",
                "encerrado": f"{i[12]}"
            })

    return dicio


def updateevento(bd, id, titulo, descricao, palestrante, data, horario, duracao, local,
                 quantidade_vagas, info_complementar, token_evento, encerrado):

    bd.cursor.execute("UPDATE [dbo].[evento] SET [titulo]='{}',"
                      "[descricao]='{}', [palestrante]='{}', [data]='{}', [horario]='{}', [duracao]='{}',"
                      "[local]='{}', [quantidade_vagas]='{}', [info_complementares]='{}',"
                      "[token_evento]='{}', [encerrado]='{}' WHERE [id]={}".format(titulo,
                                                                                   descricao, palestrante, data,
                                                                                   horario, duracao, local,
                                                                                   quantidade_vagas,
                                                                                   info_complementar,
                                                                                   token_evento, encerrado, id))
    bd.cursor.commit()


def deletaevento(bd, id):
    bd.cursor.execute("DELETE FROM [dbo].[evento] WHERE [evento].[id]=ID".replace("ID", id))
    bd.cursor.commit()


def createpessoa(bd, ra, nome, sobrenome, senha, curso, tipo_pessoa, total_horas_atividade, ativo):
    bd.cursor.execute("""INSERT INTO [dbo].[pessoa] ([ra], [nome], [sobrenome], [senha], [curso], [tipo_pessoa]
                       ,[total_horas_atividades], [ativo]) VALUES('{}', '{}', '{}', '{}',
                       (SELECT id from dbo.tipo_pessoa WHERE id={}), '{}', '{}', 
                       '{}'""".format(ra, nome, sobrenome, senha, curso, tipo_pessoa, total_horas_atividade, ativo))
    bd.cursor.commit()


def readpessoa(bd, ra):
    lido = bd.cursor.execute("""SELECT * FROM [dbo].[pessoa] WHERE ra={}""".format(ra)).fetchall()
    bd.cursor.commit()
    for i in lido:
        dicio = {
            "ra": f"{i[0]}",
            "nome": f"{i[1]}",
            "sobrenome": f"{i[2]}",
            "senha": f"{i[3]}",
            "curso": f"{i[4]}",
            "tipo_pessoa": f"{i[5]}",
            "total_horas_atividades": f"{i[6]}",
            "ativo": f"{i[7]}",
        }

    return dicio


def updatepessoa(bd, ra, nome, sobrenome, senha, curso, tipo_pessoa, total_horas_atividade, ativo):
    bd.cursor.execute("""
            UPDATE [dbo].[pessoa]
       SET [nome] = '{}'
          ,[sobrenome] = '{}'
          ,[senha] = '{}'
          ,[curso] = '{}'
          ,[tipo_pessoa] = '{}'
          ,[total_horas_atividades] = '{}'
          ,[ativo] = '{}'
     WHERE ra = '{}'
    """.format(ra, nome, sobrenome, senha, curso, tipo_pessoa, total_horas_atividade, ativo))
    bd.cursor.commit()


def deletepessoa(bd, ra):
    bd.cursor.execute("""
        DELETE FROM [dbo].[pessoa]
        WHERE ra='{}'
    """.format(ra))
    bd.cursor.commit()


def createcategoria_atividade(bd, id, titulo, descricao):
    bd.cursor.execute("""
    INSERT INTO [dbo].[categoria_atividade]
           ([titulo],[descricao])
     VALUES
       ('{}', '{}')""".format(titulo, descricao))
    bd.cursor.commit()


def readcategoria_atividade(bd):
    dicio = []
    lido = bd.cursor.execute("""
    SELECT * FROM [dbo].[categoria_atividade]
    """).fetchall()
    bd.cursor.commit()
    for i in lido:
        dicio.append({
            "id": f"{i[0]}",
            "titulo": f"{i[1]}",
            "descricao": f"{i[2]}"
        })
    return dicio