# Quickstart — Para quien nunca ha programado

> Esta guía es para creadores de contenido, marketers y founders que quieren usar los frameworks de Kallaway con Claude — sin escribir código.

---

## ¿Qué es esto, en una frase?

Son **7 "manuales" para Claude** (la IA) que le enseñan a pensar como Kane Kallaway cuando le pides ayuda con tu contenido. En vez de copiar y pegar prompts cada vez, le hablas normal y Claude aplica los frameworks correctos automáticamente.

---

## ¿Qué necesitas?

Una cuenta de Claude. Cualquiera de estas tres opciones sirve — elige la que ya uses:

| Si usas… | Cómo lo vas a usar |
|---|---|
| **Claude.ai (web/desktop)** | Pegas el contenido de la skill en un "Project" y listo |
| **Claude Code (terminal)** | Descomprimes los archivos `.skill` en una carpeta — toma 30 segundos |
| **Nada todavía** | Crea cuenta gratis en [claude.ai](https://claude.ai) y sigue la opción web |

---

## Opción A — Claude.ai (la más simple, sin terminal)

**Tiempo: 5 minutos por skill.**

1. Ve a [claude.ai](https://claude.ai) e inicia sesión
2. Click en **"Projects"** (en el menú lateral) → **"Create Project"**
3. Nómbralo: `Kallaway - Hooks` (o el que vayas a usar)
4. En este repositorio abre `skills/kallaway-hooks/SKILL.md` ([link directo](https://github.com/anthonysurfermx/creator-knowledge-engine/blob/main/skills/kallaway-hooks/SKILL.md))
5. Copia **todo el contenido** del archivo
6. En tu Project de Claude, pega ese contenido en el campo **"Custom instructions"**
7. Guarda
8. Empieza a chatear dentro de ese Project — Claude ya tiene la skill activa

Repite el proceso por cada una de las 7 skills (o solo las que necesites — los hooks son los más útiles para empezar).

> 💡 **Tip:** crea un Project distinto por skill. Así no se mezclan los frameworks y Claude aplica el correcto según el Project en el que estés.

---

## Opción B — Claude Code (terminal, más potente)

**Tiempo: 2 minutos para las 7 skills de un jalón.**

Si ya tienes [Claude Code](https://claude.ai/claude-code) instalado:

1. Abre la Terminal (Mac) o PowerShell (Windows)
2. Pega esto y dale Enter:

```bash
git clone https://github.com/anthonysurfermx/creator-knowledge-engine.git
cd creator-knowledge-engine
mkdir -p ~/.claude/skills
for f in packaged/*.skill; do
  unzip -o "$f" -d ~/.claude/skills/
done
```

3. Abre Claude Code en cualquier proyecto. Las skills se activan solas cuando escribes cosas como "escribe un hook" o "diseña un thumbnail".

---

## Cómo se usa (ejemplos reales para copy-paste)

Una vez instalado, le hablas a Claude normal. No tienes que decir "usa la skill X" — Claude detecta qué necesitas por las palabras que uses.

### Ejemplo 1 — Hook para un video

> **Tú:** Estoy haciendo un video sobre por qué los mexicanos están comprando USDC en vez de dólares. Dame 3 variaciones de hook usando el arquetipo Investigator y otro contrarian. En español, tono natural.

**Lo que obtienes:** 3 hooks completos con visual hook, spoken hook, texto en pantalla y audio sugerido — alineados a la fórmula de 3 pasos de Kallaway.

### Ejemplo 2 — Validar una idea antes de grabar

> **Tú:** ¿Esta idea tiene potencial viral? "Tutorial de cómo configurar una wallet de Solana en 5 minutos". Audiencia: principiantes en LATAM.

**Lo que obtienes:** análisis con los 9 atributos de contenido viral, score de outlier, y sugerencias para reformular el ángulo si está débil.

### Ejemplo 3 — Título y thumbnail

> **Tú:** Necesito 5 títulos y un concepto de thumbnail para un video largo sobre "cómo monetizar contenido de cripto sin patrocinios". CTR es la prioridad.

**Lo que obtienes:** títulos optimizados con el Trust Score Model + descripción visual del thumbnail con las 7 categorías de "stun gun".

### Ejemplo 4 — Guión completo

> **Tú:** Escríbeme el guión para un Reel de 60 segundos sobre Bitcoin L2s. Audiencia LATAM, tono educativo pero divertido.

**Lo que obtienes:** guión con Story Ladder, pacing, re-hooks cada 8-10 segundos y CTA al final.

---

## ¿Cuál skill sirve para qué? (chuleta rápida)

| Si lo que necesitas es… | Pídele esto |
|---|---|
| Que la gente NO haga scroll | "Dame un hook para…" |
| Estructurar un video largo | "Escribe el guión para…" |
| Saber si una idea va a pegar | "¿Esta idea tiene potencial viral?…" |
| Más views (título + thumb) | "Dame títulos y thumbnail para…" |
| Una rutina de producción | "Diséñame un workflow para postear 3x por semana" |
| Cómo cobrar por tu contenido | "¿Cómo monetizo X seguidores en…?" |
| Adaptar a cada red social | "¿Cómo posteo esto en LinkedIn vs Twitter vs YouTube?" |

---

## Preguntas frecuentes

**¿Tengo que pagar Claude?**
La versión gratis de Claude.ai funciona. Si vas a generar mucho contenido, el plan Pro ($20/mes) te da más mensajes.

**¿Las skills funcionan en español?**
Sí. Todos los frameworks están en inglés pero Claude los aplica a cualquier idioma — solo pídelo en español.

**¿Puedo usar esto para otro nicho que no sea cripto/AI?**
Sí. Los frameworks son universales. Solo cambia tu tema en el prompt.

**¿Esto reemplaza estudiar a Kallaway?**
No. Es un atajo para aplicar sus frameworks rápido. Si te interesa el tema, ver sus videos sigue valiendo la pena — pero ya no tienes que memorizar nada.

**¿Cómo sé qué skill se activó?**
En Claude Code, te lo dice. En Claude.ai con Projects, se aplica la que pusiste en custom instructions.

---

## ¿Algo no funciona?

Abre un issue en [GitHub](https://github.com/anthonysurfermx/creator-knowledge-engine/issues) con captura de pantalla del problema.
