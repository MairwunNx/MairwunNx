# Pavel Erokhin

Software engineer and architect in Madrid, focused on AI agents and the tooling around them: agent harnesses, MCP servers, and LLM evaluation.

In engineering since 2017. I’ve designed and built high-load mobile and backend systems at Wildberries (100M+ MAU), Guava Pay, Alfa-Bank, and MTS Bank.

### AI agents

- **[Allay](https://allay.chat)**: an AI helper for Minecraft servers, on my own agent harness with tools, sub-agents, memory, and OpenTelemetry traces.
- **[ctxray](https://github.com/MairwunNx/ctxray)**: shows what Claude Code, Codex, and Cursor load into the model’s context and tests it in CI, including skill-selection evaluation against real models.
- **[minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)**: an MCP server with 51 tools and token-scoped permissions.
- **[Xi](https://github.com/MairwunNx/xi)**: a multimodal AI assistant for Telegram, with text, voice, and images across five LLM providers and memory across sessions.

### Architecture

- **[Capsa](https://github.com/MairwunNx/Capsa)**: the engine behind Capability Slice Architecture, my architecture for declarative UI, where each capability owns one slice of state and one user scenario.
- **[Feature-Action Architecture](https://github.com/MairwunNx/Feature-Action-Architecture)**: a backend architecture with vertical slices by business domain and actions instead of service classes.

### Systems programming and reverse engineering

Built on JVM and Android Runtime (ART) internals: garbage collection, JIT compilation, and profiling with Java Flight Recorder.

- **[ancaria](https://ancaria.dev)**: a mod loader for Sacred Gold (2004), with hooks only in memory and a Rust bridge to the JVM.
- **[Bytekodex](https://github.com/bytekodex)**: a Rust engine that renders JVM bytecode as images.

### Backend, infrastructure, and observability

- **[WorldAPI](https://github.com/MairwunNx/minecraft-worldapi)**: a Minecraft server on HTTP, with 129 REST operations, OpenAPI, and a WebSocket event feed.
- **[minecraft-exporter](https://github.com/MairwunNx/minecraft-exporter)**: a Prometheus exporter in Go that turns a Minecraft server into metrics.
- **[minecraft-grafana](https://github.com/MairwunNx/minecraft-grafana)**: a Grafana dashboard for those metrics, from tick times and garbage collection to players and chat, [published on grafana.com](https://grafana.com/grafana/dashboards/25941-minecraft-server-minecraft-exporter/).
- **[Electronic Shop Demo](https://github.com/Electronic-Shop-Demo)**: a showcase shop with a Spring Boot backend on PostgreSQL, MongoDB, and Redis, a Micronaut analytics service, and Android, JavaFX, and Electron clients.

Some projects here are finished, some are in active development, and others are no longer maintained.

<p align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/kotlin/kotlin-original.svg" height="36" alt="Kotlin" title="Kotlin" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/java/java-original.svg" height="36" alt="Java" title="Java" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/typescript/typescript-original.svg" height="36" alt="TypeScript" title="TypeScript" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/go/go-original-wordmark.svg" height="36" alt="Go" title="Go" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/android/android-original.svg" height="36" alt="Android" title="Android" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/jetpackcompose/jetpackcompose-original.svg" height="36" alt="Jetpack Compose" title="Jetpack Compose" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/bun/bun-original.svg" height="36" alt="Bun" title="Bun" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/gradle/gradle-original.svg" height="36" alt="Gradle" title="Gradle" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/docker/docker-original.svg" height="36" alt="Docker" title="Docker" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/postgresql/postgresql-original.svg" height="36" alt="PostgreSQL" title="PostgreSQL" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/redis/redis-original.svg" height="36" alt="Redis" title="Redis" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/prometheus/prometheus-original.svg" height="36" alt="Prometheus" title="Prometheus" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/grafana/grafana-original.svg" height="36" alt="Grafana" title="Grafana" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons/cloudflare/cloudflare-original.svg" height="36" alt="Cloudflare" title="Cloudflare" />
</p>

<p align="left">
  <b>Fueled by</b>
  <a href="https://www.redbull.com">
    <img src="https://img.shields.io/badge/Red_Bull-%23E30613.svg?style=for-the-badge&logo=red-bull&logoColor=white" valign="middle" alt="Red Bull" />
  </a>
</p>

---

<details>
<summary>Русская версия</summary>

# Павел Ерохин

Инженер-программист и архитектор из Мадрида. Специализируюсь на ИИ-агентах и инструментах вокруг них: ИИ-харнессах, MCP-серверах и оценке качества LLM.

В разработке с 2017 года. Проектировал и разрабатывал высоконагруженные мобильные и серверные системы в Wildberries (100M+ MAU), Guava Pay, Альфа-Банке и МТС Банке.

### ИИ-агенты

- **[Allay](https://allay.chat)** — ИИ-помощник для серверов Minecraft на собственном харнессе: тулы, субагенты, память и трассировка в OpenTelemetry.
- **[ctxray](https://github.com/MairwunNx/ctxray)** — показывает, что Claude Code, Codex и Cursor загружают в контекст модели, и проверяет это в CI, включая оценку выбора скиллов на реальных моделях.
- **[minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)** — MCP-сервер на 51 тул с правами доступа по токену.
- **[Xi](https://github.com/MairwunNx/xi)** — мультимодальный ИИ-ассистент для Telegram: текст, голос и изображения через пять LLM-провайдеров, память между сессиями.

### Архитектура

- **[Capsa](https://github.com/MairwunNx/Capsa)** — движок моей Capability Slice Architecture, архитектуры декларативного UI, в которой каждая возможность (capability) владеет своим срезом состояния и одним пользовательским сценарием.
- **[Feature-Action Architecture](https://github.com/MairwunNx/Feature-Action-Architecture)** — архитектура бэкенда: вертикальные срезы по бизнес-доменам и действия (actions) вместо сервисных классов.

### Системное программирование и реверс-инжиниринг

Опираюсь на знание внутреннего устройства JVM и Android Runtime (ART): сборки мусора, JIT-компиляции, профилирования через Java Flight Recorder.

- **[ancaria](https://ancaria.dev)** — загрузчик модов для Sacred Gold (2004): хуки только в памяти и мост на Rust до JVM.
- **[Bytekodex](https://github.com/bytekodex)** — движок на Rust, который рисует байткод JVM.

### Бэкенд, инфраструктура и наблюдаемость

- **[WorldAPI](https://github.com/MairwunNx/minecraft-worldapi)** — Minecraft-сервер через HTTP: 129 REST-операций, OpenAPI и WebSocket-поток событий.
- **[minecraft-exporter](https://github.com/MairwunNx/minecraft-exporter)** — экспортер Prometheus на Go, который превращает Minecraft-сервер в метрики.
- **[minecraft-grafana](https://github.com/MairwunNx/minecraft-grafana)** — дашборд Grafana для этих метрик, от времени тика и сборки мусора до игроков и чата, [опубликован на grafana.com](https://grafana.com/grafana/dashboards/25941-minecraft-server-minecraft-exporter/).
- **[Electronic Shop Demo](https://github.com/Electronic-Shop-Demo)** — демонстрационный магазин: бэкенд на Spring Boot с PostgreSQL, MongoDB и Redis, сервис аналитики на Micronaut, клиенты на Android, JavaFX и Electron.

Часть проектов здесь завершена, часть в разработке, а некоторые я больше не поддерживаю.

</details>

<details>
<summary>Versión en español</summary>

# Pavel Erokhin

Ingeniero de software y arquitecto en Madrid, centrado en agentes de IA y las herramientas a su alrededor: agent harnesses, servidores MCP y evaluación de LLM.

En la ingeniería desde 2017. He diseñado y desarrollado sistemas móviles y backend de alta carga en Wildberries (más de 100M de MAU), Guava Pay, Alfa-Bank y MTS Bank.

### Agentes de IA

- **[Allay](https://allay.chat)**: un asistente de IA para servidores de Minecraft sobre mi propio agent harness, con herramientas, subagentes, memoria y trazas de OpenTelemetry.
- **[ctxray](https://github.com/MairwunNx/ctxray)**: muestra lo que Claude Code, Codex y Cursor cargan en el contexto del modelo y lo prueba en CI, incluida la evaluación de la selección de skills con modelos reales.
- **[minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)**: un servidor MCP con 51 herramientas y permisos por token.
- **[Xi](https://github.com/MairwunNx/xi)**: un asistente de IA multimodal para Telegram, con texto, voz e imágenes a través de cinco proveedores de LLM y memoria entre sesiones.

### Arquitectura

- **[Capsa](https://github.com/MairwunNx/Capsa)**: el motor de Capability Slice Architecture, mi arquitectura para UI declarativa, en la que cada capacidad gestiona una porción del estado y un escenario de usuario.
- **[Feature-Action Architecture](https://github.com/MairwunNx/Feature-Action-Architecture)**: una arquitectura de backend con porciones verticales por dominio de negocio y acciones en lugar de clases de servicio.

### Programación de sistemas e ingeniería inversa

Basada en los componentes internos de la JVM y de Android Runtime (ART): recolección de basura, compilación JIT y perfilado con Java Flight Recorder.

- **[ancaria](https://ancaria.dev)**: un cargador de mods para Sacred Gold (2004), con hooks solo en memoria y un puente en Rust hacia la JVM.
- **[Bytekodex](https://github.com/bytekodex)**: un motor en Rust que dibuja bytecode de la JVM.

### Backend, infraestructura y observabilidad

- **[WorldAPI](https://github.com/MairwunNx/minecraft-worldapi)**: un servidor de Minecraft sobre HTTP, con 129 operaciones REST, OpenAPI y un flujo de eventos por WebSocket.
- **[minecraft-exporter](https://github.com/MairwunNx/minecraft-exporter)**: un exportador de Prometheus en Go que convierte un servidor de Minecraft en métricas.
- **[minecraft-grafana](https://github.com/MairwunNx/minecraft-grafana)**: un dashboard de Grafana para esas métricas, desde los tiempos de tick y la recolección de basura hasta los jugadores y el chat, [publicado en grafana.com](https://grafana.com/grafana/dashboards/25941-minecraft-server-minecraft-exporter/).
- **[Electronic Shop Demo](https://github.com/Electronic-Shop-Demo)**: una tienda de demostración con un backend en Spring Boot sobre PostgreSQL, MongoDB y Redis, un servicio de analítica en Micronaut y clientes para Android, JavaFX y Electron.

Algunos proyectos están terminados, otros siguen en desarrollo y algunos ya no reciben mantenimiento.

</details>

---

[t.me/mairwunnx](https://t.me/mairwunnx) · [mairwunnx.com](https://mairwunnx.com)
