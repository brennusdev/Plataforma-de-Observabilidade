# Arquitetura

## Fluxo

```text
Host / Application
       |
       v
Collectors
       |
       v
Processing
       |
       v
PostgreSQL
       |
       v
FastAPI
       |
       v
Dashboard
```

## Responsabilidades

### Collectors
Responsáveis por obter dados brutos.

### Services
Aplicam regras de negócio e persistem dados.

### Models
Representam entidades persistidas no banco.

### API
Expõe os dados através de endpoints HTTP.

### Dashboard
Consumidor da API responsável pela visualização.

## Princípio

A plataforma deve evoluir sem misturar coleta, persistência, regra de negócio e apresentação.
