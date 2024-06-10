## Avaliação de Competências: Desenvolvimento de uma API Pokédex

### Objetivo
Criar uma API em Python usando FastAPI para gerenciar uma Pokédex, que lista todos os Pokémon capturados com paginação. Além disso, desenvolver uma interface de usuário simples para a Pokédex usando React + Redux ou Angular como framework de escolha.

### Requisitos da API
1. **URL Base**: Obter dados de `https://pokeapi.co/api/v2/pokemon`.
2. **Paginação**: Implementar paginação; o comportamento padrão deve listar todos os Pokémon se nenhum deslocamento ou limite for especificado.
3. **Visualização Detalhada**: Implementar uma página de detalhes para cada Pokémon similar a `https://www.pokemon.com/us/pokedex`.
4. **Busca de Dados**:
   - Utilizar `httpx` para busca de dados.
   - Garantir que os dados obtidos sejam suficientes para replicar os detalhes encontrados em `https://www.pokemon.com/us/pokedex`.
5. **Ordenação**: Os resultados da API devem ser ordenados alfabeticamente pelo nome do Pokémon.
6. **Funcionalidade de Exportação**: Capacidade de exportar a lista de Pokémon ordenada para um arquivo XML.
7. **Documentação**:
   - Fornecer documentação da API usando Swagger.
   - Seguir as melhores práticas no desenvolvimento de API.

### Requisitos do Frontend
1. **Tecnologias**: Usar React + Redux ou Angular.
2. **Funcionalidades**: A interface deve permitir a visualização da lista de Pokémon e dos detalhes de cada Pokémon individualmente.

### Desafios Adicionais
1. **Concorrência**:
   - Implementar todas as tarefas assíncronas usando corotinas.
   - Utilizar semáforo para gerenciar a concorrência.
   - Aplicar condições de corrida quando aplicável.
2. **Otimização**: Otimizar o desempenho da API sempre que possível.
3. **Persistência de Dados**: Armazenar os dados dos Pokémon obtidos em um banco de dados relacional.
4. **Testes**:
   - Escrever testes automatizados abrangentes usando pytest.
5. **Conteinerização**:
   - Conteinerizar a aplicação e gerenciá-la com Docker Compose.
6. **Integração com a Nuvem**:
   - Demonstrar expertise em nuvem implantando a API na AWS ou Google Cloud Platform.
7. **CI/CD**:
   - Configurar integração e entrega contínua com GitHub Actions.

### Diretrizes de Submissão
- Fornecer um repositório no GitHub com instruções claras no README sobre como configurar e executar a aplicação.
- Garantir que a aplicação seja implantável com configuração mínima, usando Docker e Docker Compose.

Esta avaliação de competências é projetada para testar habilidades de frontend e backend, focando em práticas modernas de desenvolvimento web e na capacidade de lidar com aplicações intensivas em dados de forma eficiente.
