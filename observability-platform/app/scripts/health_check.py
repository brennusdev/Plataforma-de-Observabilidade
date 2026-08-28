"""
Health check externo da plataforma.

Pode ser utilizado por:

- CI/CD
- Docker
- Kubernetes
- scripts operacionais
- monitoramento externo
"""

import sys

import urllib.request


URL = (
    "http://localhost/"
    "health/ready"
)


def main():

    try:

        with urllib.request.urlopen(
            URL,
            timeout=5,
        ) as response:

            if response.status == 200:

                print(
                    "Platform is READY."
                )

                return 0

    except Exception as exc:

        print(
            "Platform is NOT READY."
        )

        print(
            f"Error: {exc}"
        )

    return 1


if __name__ == "__main__":

    sys.exit(
        main()
    )