# Manifiesto de assets · build temporal

| Slot | Tema / viewport | Fuente temporal | Tratamiento | Sustitución esperada |
|---|---|---|---|---|
| Logo | claro | `logo-digizen-horizontal-light.svg` | `contain`, horizontal | Logo oficial oscuro/transparente. |
| Logo | oscuro | `logo-digizen-horizontal-dark.svg` | `contain`, horizontal | Logo oficial claro/transparente. |
| Hero | desktop | Picsum seed `digizen-hero` | 4:5, `cover` | Escena familiar sin culpa. |
| Hero | tablet/móvil | Picsum seed `digizen-hero-mobile` | 16:9 independiente | Variante horizontal producida. |
| Beat 1 | desktop | Picsum seed `digizen-relief` | 4:5 | Gesto humano de alivio. |
| Beat 1 | tablet/móvil | Picsum seed `digizen-relief-mobile` | 16:9 independiente | Variante horizontal producida. |
| Beat 2 detalle | desktop | Picsum seed `digizen-distance-detail` | 1:1 | Detalle de la misma escena final. |
| Beat 2 distancia | desktop | Picsum seed `digizen-distance-space` | 4:5 | Vacío emocional de la misma escena. |
| Beat 2 | tablet/móvil | Picsum seed `digizen-distance-mobile` | 16:9 independiente | Variante horizontal producida. |
| Beat 4 | todos | Composición UI/CSS | `feed → pausa → criterio` | Puede conservarse o recibir arte final por capas. |
| Beat 5 | todos | Preview UI neutral | 16:10 aproximado | Captura real del chat ADA. |
| Seguridad · introducción | desktop | Picsum seed `digizen-ai-safety` | 3:4 | Imagen editorial sobre seguridad y acompañamiento. |
| Seguridad | todos | Picsum seed `digizen-ada-guards` | 4:3 | Diagrama ADA + cuatro guardas. |
| Beat 6 | desktop | Picsum seed `digizen-presence` | 4:5 | Pinky promise original. |
| Beat 6 | tablet/móvil | Picsum seed `digizen-presence-mobile` | 16:9 independiente | Variante horizontal del acuerdo. |

Las URLs de Picsum son deterministas y no contienen copy. Todos los slots declaran dimensiones para reducir layout shift.
