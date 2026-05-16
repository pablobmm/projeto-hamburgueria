from apps.app import app, db_serv 
from apps.lanche.model_lanche import Lanche
from apps.categoria.model_categoria import Categoria 

def seed_database():
    """Popula a tabela de lanches com dados de exemplo."""

    categorias_nomes = ["Burgers", "Pizza", "Vegetariano", "Kids"]
    cat_objetos = {}

    print("Verificando/Inserindo categorias...")
    for nome in categorias_nomes:
        categoria = Categoria.query.filter_by(nome=nome).first()
        if not categoria:
            categoria = Categoria(nome=nome)
            db_serv.session.add(categoria)
            db_serv.session.flush() 
            print(f"Categoria criada: {nome}")
        cat_objetos[nome] = categoria

    lanches_de_exemplo = [
        {
            "id": 1, "nome": "Java Burguer", "preco": 31.99, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger1.png",
            "descricao": "Pão com gergelim, um suculento hambúrguer de pura carne bovina, cheddar fatiado, molho barbecue, 6 deliciosas onion rings, tomate, alface e maionese."
        },
        {
            "id": 2, "nome": "Kotlin Burguer", "preco": 36.5, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger2.png",
            "descricao": "Pão com gergelim, dois suculentos hambúrgueres de pura carne bovina, duas fatias de cheddar, quatro fatias de picles, alface, tomate, cebola, maionese e ketchup."
        },
        {
            "id": 3, "nome": "Python Burguer", "preco": 33.99, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger3.png",
            "descricao": "Pão com gergelim, um saboroso hambúrguer de pura carne bovina, uma fatia de queijo cheddar, duas fatias de picles, ketchup e molho mostarda."
        },
        {
            "id": 4, "nome": "SQL Burguer", "preco": 39.99, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger4.png", 
            "descricao": "Um hambúrguer (carne 100% bovina), bacon, alface americana, cebola, queijo processado sabor cheddar, tomate, maionese, ketchup, mostarda e pão com gergelim."
        },
        {
            "id": 5, "nome": "PHP Burguer", "preco": 30.99, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger5.png", 
            "descricao": "Dois hambúrgueres (carne 100% bovina), queijo processado sabor cheddar, cebola, fatias de bacon, ketchup, mostarda e pão com gergelim."
        },
        {
            "id": 6, "nome": "JS Burguer", "preco": 36.99, "categoria_id": cat_objetos["Burgers"].id,
            "imagem": "burger6.png", 
            "descricao": "Dois hambúrgueres de carne 100% bovina, maionese com sabor de carne defumada, fatias de bacon, queijo processado, molho especial e cebola ao molho shoyu."
        },
        {
            "id": 10, "nome": "Pizza Pythonresa", "preco": 45.90, "categoria_id": cat_objetos["Pizza"].id,
            "imagem": "pizza10.png", 
            "descricao": "Molho de tomate, mussarela, calabresa e cebola."
        },
        {
            "id": 11, "nome": "Pizza Marguerita", "preco": 42.00, "categoria_id": cat_objetos["Pizza"].id,
            "imagem": "pizza11.png", 
            "descricao": "Molho de tomate, mussarela, manjericão fresco e tomate."
        },
        {
            "id": 20, "nome": "Veggie Node", "preco": 29.90, "categoria_id": cat_objetos["Vegetariano"].id,
            "imagem": "vegetariano20.png", 
            "descricao": "Hambúrguer de grão de bico, alface, tomate e molho de ervas."
        },
        {
            "id": 30, "nome": "Júnior Script", "preco": 19.90, "categoria_id": cat_objetos["Kids"].id,
            "imagem": "kids30.png", 
            "descricao": "Cheeseburger pequeno, batata frita e suco de laranja."
        }
    ]

    print("Inserindo dados de exemplo de lanches...")
    for dados_lanche in lanches_de_exemplo:
        lanche_existente = db_serv.session.get(Lanche, dados_lanche["id"])
        if not lanche_existente:
            novo_lanche = Lanche(**dados_lanche)
            db_serv.session.add(novo_lanche)
            print(f"Adicionado: {dados_lanche['nome']}")
            
    db_serv.session.commit()
    print("Dados de exemplo inseridos com sucesso.")

def init():
    with app.app_context():
        print("--- INICIANDO PROCESSO DE MANUTENÇÃO DO BANCO ---")
        db_serv.drop_all()
                
        print("1. Criando tabelas (com a nova coluna imagem)...")
        db_serv.create_all() 
        
        print("2. Verificando se precisa de dados iniciais...")
        seed_database()
        
        print("--- BANCO DE DADOS PRONTO! ---")
        
if __name__ == "__main__":
    init()