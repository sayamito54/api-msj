# GitHub Actions - CI/CD Pipeline

Este proyecto incluye un pipeline completo de CI/CD configurado con GitHub Actions para automatizar el desarrollo, testing y deployment.

## 🚀 Workflows Disponibles

### 1. CI/CD Pipeline Principal (`ci-cd.yml`)

**Triggers:**
- Push a `main` o `develop`
- Pull Requests a `main` o `develop`
- Manual (`workflow_dispatch`)

**Jobs:**
- **Quality & Testing**: Linting, type checking, tests y coverage
- **Security Scan**: Análisis de vulnerabilidades con Safety
- **Build & Integration**: Tests de integración y build
- **Deploy to Production**: Deployment automático (solo en `main`)
- **Notify Team**: Notificaciones de éxito/fallo

### 2. Test Suite (`test.yml`)

**Triggers:**
- Push a `main` o `develop`
- Pull Requests a `main` o `develop`

**Características:**
- Testing en múltiples versiones de Python (3.9, 3.10, 3.11)
- Generación de reportes de coverage
- Cache de dependencias para optimización

### 3. Deploy to Staging (`deploy-staging.yml`)

**Triggers:**
- Push a `develop`
- Manual (`workflow_dispatch`)

**Características:**
- Deployment automático a ambiente de staging
- Smoke tests antes del deployment
- Health checks post-deployment

## 🛠️ Herramientas de Calidad

### Code Quality
- **Black**: Formateo de código
- **Flake8**: Linting y análisis estático
- **MyPy**: Type checking
- **isort**: Organización de imports

### Testing
- **pytest**: Framework de testing
- **pytest-cov**: Coverage reports
- **pytest-asyncio**: Soporte para async tests

### Security
- **Safety**: Análisis de vulnerabilidades en dependencias

## 📋 Configuración Requerida

### 1. Secrets de GitHub

Configura estos secrets en tu repositorio (`Settings > Secrets and variables > Actions`):

```bash
# Para deployment
DEPLOY_SSH_KEY          # Clave SSH para el servidor
DEPLOY_HOST             # Host del servidor
DEPLOY_USER             # Usuario del servidor
DEPLOY_PATH             # Ruta de deployment

# Para notificaciones (opcional)
SLACK_WEBHOOK_URL       # Webhook de Slack
DISCORD_WEBHOOK_URL     # Webhook de Discord
```

### 2. Environments

Configura estos environments en tu repositorio:

- **staging**: Para deployment de staging
- **production**: Para deployment de producción

### 3. Branch Protection Rules

Recomendado configurar protección en `main`:
- Requerir status checks
- Requerir pull request reviews
- Requerir conversación de PR

## 🔧 Uso Local

### Instalar dependencias de desarrollo

```bash
pip install -r requirements-dev.txt
```

### Ejecutar herramientas de calidad

```bash
# Formatear código
black .

# Linting
flake8 .

# Type checking
mypy app/

# Tests
pytest tests/ -v --cov=app
```

### Pre-commit hooks (recomendado)

```bash
pip install pre-commit
pre-commit install
```

## 📊 Monitoreo

### Coverage Reports
- Los reportes de coverage se generan automáticamente
- Se suben como artifacts en cada workflow
- Integración opcional con Codecov

### Notificaciones
- Los workflows notifican automáticamente el estado
- Se pueden configurar webhooks para Slack/Discord
- Emails automáticos para el equipo

## 🚨 Troubleshooting

### Workflow no se ejecuta
1. Verificar que estés en la rama correcta (`main` o `develop`)
2. Verificar que el archivo esté en `.github/workflows/`
3. Verificar sintaxis YAML del workflow

### Tests fallan
1. Ejecutar tests localmente: `pytest tests/ -v`
2. Verificar dependencias: `pip install -r requirements.txt`
3. Verificar configuración de entorno

### Deployment falla
1. Verificar secrets de GitHub
2. Verificar conectividad SSH al servidor
3. Verificar permisos de usuario en servidor

## 🔄 Flujo de Trabajo Recomendado

1. **Desarrollo**: Trabajar en rama `feature/`
2. **Testing**: Crear PR a `develop`
3. **Staging**: Merge a `develop` → Auto-deploy a staging
4. **Production**: Merge `develop` a `main` → Auto-deploy a producción

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)
