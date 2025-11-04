# Plataforma de Fidelidade e Vendas Online - Code Burguer

## 📝 Propósito e Ideia Geral

Este projeto é uma **Plataforma de Fidelidade e Vendas Online** desenvolvida para a **Code Burguer**. A iniciativa visa mitigar a dependência de plataformas de delivery de terceiros, que cobram altas taxas e limitam a autonomia do negócio. A ideia principal é criar um canal de vendas direto e um programa de fidelidade robusto, permitindo que a hamburgueria construa um relacionamento duradouro com seus clientes e recupere a margem de lucro.

O sistema se destina a:
* **Usuários Finais (Clientes):** Para que possam visualizar o cardápio, personalizar pedidos e participar de um programa de recompensas de forma simples e intuitiva.
* **Administradores da Hamburgueria:** Para que possam gerenciar pedidos, acompanhar o desempenho de vendas e obter dados valiosos sobre o comportamento do cliente.

---

## 🚀 Como Rodar a Aplicação

Siga os passos abaixo para configurar e rodar a API localmente:

### Pré-requisitos
* Node.js (versão 18 ou superior)
* npm (gerenciador de pacotes do Node.js)
* Docker
* Uma IDE como VS Code ou WebStorm

### Passos
1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/devgbrviana/projeto-hamburgueria.git
    cd projeto-hamburgueria
    ```
2.  **Configurar o Banco de Dados:**
    * Use o Docker para iniciar o banco de dados. Certifique-se de que a porta 5432 (ou a porta padrão do seu banco de dados) está livre.
    * Esses comandos irão inicializar o banco de dados e buildar a aplicação, executando o script init_db.py que cira as tabelas no MySQL.
      ```bash
      docker-compose build --no-cache api
      docker-compose run --rm api python -m apps.init_db
      ```
    * Rodar a Aplicação
    * Ele inicia a aplicação completa, subindo o contâiner
    * do MySQL (COm as tabelas já criadas)
      ```bash
      docker-compose up
      ```

A API estará rodando em `http://localhost:3000`.

---

## ⚙️ Stack e Tecnologias

O projeto foi construído utilizando as seguintes tecnologias:

* **Back-end:** Node.js com Express
* **Banco de Dados:** PostgreSQL (containerizado com Docker)
* **ORM:** Sequelize
* **Autenticação:** JWT (JSON Web Tokens)
* **Testes:** Jest
* **Ferramentas de Desenvolvimento:** Docker, Git

---

## 📈 Diagrama Entidade-Relacionamento (ER)

O modelo do banco de dados foi projetado para ser robusto e escalável. O diagrama ER foi desenvolvido usando o software **Astah** e pode ser visualizado abaixo. Ele descreve as entidades e seus relacionamentos, incluindo a entidade associativa **Pedido** que resolve a relação de muitos-para-muitos entre **Usuário** e **Lanche**.

<img width="1062" height="573" alt="image" src="https://github.com/user-attachments/assets/dd44dde5-4971-41b7-98f4-a591cf84e392" />


---
