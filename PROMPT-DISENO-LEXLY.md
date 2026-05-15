# Prompt para Diseño UI/UX - Lexly SaaS

## 📋 Contexto del Proyecto

**Nombre:** Lexly SaaS
**Tipo:** Web App SaaS para gestión de casos legales de inmigración
**Descripción:** Sistema de gestión integral para estudios de abogados de inmigración. Administra clientes, casos legales, documentos y citas.
**Usuario objetivo:** Estudios jurídicos pequeños/medianos de inmigración

---

## 🎨 Personalidad de Marca: "8bits-estudio"

- **Estilo:** Minimalista, profesional, moderno
- **Valores:** Precisión, claridad, eficiencia
- **Tono:** Serio pero accesible, confiado sin ser arrogante
- **Identidad:** Tecnología al servicio del derecho

---

## 📱 Requisitos Funcionales

### Pantallas Necesarias

1. **Login** - Email/password, diseño limpio centrado
2. **Dashboard** - Vista general con métricas rápidas
3. **Clientes**
   - Listado con búsqueda/filtros
   - Ficha de cliente (detalle)
   - Modal crear/editar cliente
4. **Casos**
   - Listado con filtros por estado
   - Ficha de caso
   - Modal crear/editar caso
   - Vista de casos por cliente
5. **Documentos** (proximamente)
6. **Citas** (proximamente)

---

## 🎯 Requisitos UX/UI

### Principios de Diseño

- ✅ **Minimalismo:** Solo éléments necesarios
- ✅ **Jerarquía clara:** Lo importante destaca
- ✅ ** Feedback inmediato:** El usuario sabe qué pasó
- ✅ **Espacio blanco:** Breathing room entre elementos
- ✅ **Tipografía legible:** Fuentes modernas (Inter, SF Pro, etc.)
- ✅ **Espaciado consistente:** Múltiplos de 4px u 8px

### Color palette Sugerida

| Propósito | Color |
|---------|-------|
| Primary | #1E3A5F (azul profundo profesional) |
| Accent | #00D4AA (verde esmeralda moderno) |
| Fondo | #F8FAFB / #FFFFFF |
| Texto | #1A1A2E |
| Estados | Success: #10B981 / Error: #EF4444 / Warning: #F59E0B |

### Componentes Requeridos

- **Navbar:** Fijo, minimal, con avatar de usuario
- **Sidebar/Tabs:** Navegaciónsecondary clara
- **Cards:** Para listados (clientes, casos)
- **Buttons:** Primary (filled), Secondary (outline), Danger
- **Forms:** Labels claros, validation inline
- **Modals:**_centerados, backdrop subtle
- **Tables:** Alternating rows, sort headers
- **Status badges:** Estados visuales diferenciados

---

## 🖥️ Especificaciones Técnicas

- **Responsive:** Mobile first, hasta 1920px
- **Framework UI suggestion:** Tailwind CSS o similar
- **Iconos:** Line icons, consistentes
- **Micro-interacciones:** Hover states, subtle transitions

---

## 📋 Entregable Esperado

1. Wireframes de cada pantalla principal
2. Design system (colors, typography, components)
3. Prototipo interactivo o specs detalladas
4. Guía de implementación

---

## 💡 Notas Adicionales

- Mantener coherencia con identidad 8bits-estudio
- Priorizar usabilidad sobre decorative
- El usuario final es abogado, no técnico - debe ser intuitivo
- Optimizar para flujo de trabajo diario