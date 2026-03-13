Sistema de Controle de Estoque
Este projeto tem como objetivo desenvolver uma aplicação para gerenciamento de estoque, permitindo o cadastro de produtos, movimentações de entrada e saída, além da administração de usuários com diferentes perfis de acesso.

Funcionalidades
Autenticação de Usuário: login com validação de credenciais.

Cadastro de Produtos: inclusão de novos itens com descrição, preço, quantidade e estoque mínimo.

Movimentação de Estoque: registro de entradas e saídas vinculadas a usuários e produtos.

Consulta de Estoque: listagem de produtos com destaque para itens abaixo do estoque mínimo.

Gestão de Usuários (ADMIN): criação de novos usuários com definição de perfil (administrador ou comum).

Modelagem
O sistema foi estruturado a partir de um modelo conceitual e modelo lógico, garantindo integridade referencial e clareza nos relacionamentos entre entidades.

Usuário ↔ Movimentação: 1:N

Produto ↔ Movimentação: 1:N

A entidade Movimentação funciona como ponte entre usuários e produtos.

Fluxograma
O fluxo da aplicação inicia com o login e validação de credenciais. Após o acesso, o Menu Principal centraliza as opções de operação (cadastro de produto, movimentação de estoque, listagem e cadastro de usuários). Cada processo retorna ao menu, e o sistema pode ser encerrado a qualquer momento pela opção “Encerrar Sistema”.

Tecnologias Utilizadas
Banco de Dados: MySQL

Modelagem: brModelo

Linguagem: Python

Ferramentas de Diagramação: Draw.io  / Lucidchart
