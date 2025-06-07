Violações das restrições REST: 

- Interface Uniforme

A rota `/obter/itens` está incorreta. Está passando um nome de ação e não uma URI de recurso.

A rota `POST /itens` também está incorreta. Ela deveria: 
- Retornar um header `location`, com a URI do novo recurso
- Retornar o ID do novo URI no corpo da resposta

A rota `/filtrar-itens` também apresenta erros de interface. Para começar, tem um nome de ação, em vez de uma URI de recurso, e, para piorar, usa `POST` para obter recurso. 

- Cliente-servidor

A rota `/filtrar-itens` também viola a restrição cliente-servidor, pois, para utilizá-la, o cliente precisa "conhecer" a implementação do servidor e passar um filtro que será utilizado para criar uma função lambda para filtrar recursos. 
