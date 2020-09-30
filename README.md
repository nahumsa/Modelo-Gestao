# Case: Uma plataforma de gestão de manutenção com formulários online e dashboard de análise dos dados.

Abordagem: Separarei esse problema em três etapas: A primeira é para a plataforma de gestão de manutenção onde será necessário criar formulários online e colocar esses formulários em uma database. A segunda etapa consiste em criar um dashboard para visualização dos dados. A terceira e última é fazer o deploy da aplicação web online para que possa ser utilizada.

[Link para o app](https://gestao-modelo.herokuapp.com/)

# Formulário

## Ferramentas: Flask, SQLAlchemy, SQLITE, HTML, CSS

Criar um template para o formulário em HTML, nesse formulário deve ter as seguintes sessões:

ID do serviço, ID do equipamento, tipo do serviço (preventivo, corretivo, planejada), data de solicitação (default o dia atual), data de início + hora de inicio, data de término + hora de término, descrição do serviço.

Para interagir com o formulário do HTML utilizo Flask para gerar o HTML e colocar os resultados do formulário na database. 

Como os dados serão estruturados escolhi o SQLite para o bancos de dados, a chave primária seria o ID do serviço, pois é único e identifica uma entrada na tabela.

Para melhorar a experiência do usuário, é possível colocar seções importantes com cores específicas.  

Após isso, é preciso criar uma forma de interagir com a database para alterar ou excluir formulários, para isso é necessário criar um novo template que mostra a database em tabela para que o formulário possa ser excluído ou alterado. Para isso, utilizo uma nova rota no flask, de forma que isso seja uma nova página com a rota '/all_tasks'.

# Dashboard

## Ferramentas: Dash e Plotly

Para o dashboard é necessário acessar a database que criamos anteriormente e demonstrar visualizações dos dados, portanto escolhi o [dash]([http://dash.plotly.com/](http://dash.plotly.com/)) para a criação do dashboard, pois esse pacote utiliza flask para gerar o dashboard e isso faz a integração entre os dois ser fácil. Para gerar os gráficos escolhi utilizar o plotly que é a biblioteca recomendada pelo dash.

Através disso, pode ser gerado gráficos e tabelas, como por exemplo:

- Gráfico mostrando a quantidade de serviços adicionados por dia e cores para cada serviço;
- Tabela com porcentagem de serviços concluídos;
- Gráfico mostrando a média semanal de serviços concluídos;
- etc.

Todos os gráficos podem ser gerados a partir da database fazendo buscas quando necessárias, dependendo to tamanho da database é possível passar as entradas da database para um dataframe do pandas, pois o Dash tem funções inerentes para esse tipo de objeto facilitando a geração de gráficos.

# Deploy

## Ferramentas: Heroku, Gunnicorn

Para efetuar o deploy da ferramenta, utilizarei o Heroku e o gunnicorn para criar o webapp.