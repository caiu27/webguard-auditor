import requests

SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "title": "HSTS (Strict-Transport-Security)",
        "risk": "Alto",
        "recommendation": "Fuerza el uso de conexiones cifradas HTTPS para prevenir ataques Man-in-the-Middle."
    },
    "Content-Security-Policy": {
        "title": "Content Security Policy (CSP)",
        "risk": "Alto",
        "recommendation": "Previene la ejecución de scripts no autorizados (XSS) y la inyección de código."
    },
    "X-Frame-Options": {
        "title": "X-Frame-Options",
        "risk": "Medio",
        "recommendation": "Protege a tus usuarios contra ataques de Clickjacking evitando que el sitio sea embebido en iframes."
    },
    "X-Content-Type-Options": {
        "title": "X-Content-Type-Options",
        "risk": "Bajo",
        "recommendation": "Evita que los navegadores interpreten archivos con tipos MIME incorrectos (MIME sniffing)."
    },
    "Referrer-Policy": {
        "title": "Referrer-Policy",
        "risk": "Bajo",
        "recommendation": "Controla la cantidad de información enviada en el encabezado Referer al navegar a otros sitios."
    },
    "Permissions-Policy": {
        "title": "Permissions-Policy",
        "risk": "Bajo",
        "recommendation": "Restringe el acceso a funciones del hardware/navegador como cámara, micrófono y geolocalización."
    }
}

def analyze_headers(target_url: str):
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        response = requests.get(target_url, timeout=10, allow_redirects=True)
        resp_headers = response.headers
    except Exception as e:
        return None, f"Error al conectar con la URL: {str(e)}"

    found_headers = {}
    missing_headers = {}

    for header, info in SECURITY_HEADERS.items():
        if header in resp_headers:
            found_headers[header] = {
                "value": resp_headers[header],
                "details": info
            }
        else:
            missing_headers[header] = info

    score = int((len(found_headers) / len(SECURITY_HEADERS)) * 100)

    results = {
        "url": target_url,
        "status_code": response.status_code,
        "score": score,
        "found": found_headers,
        "missing": missing_headers
    }

    return results, None