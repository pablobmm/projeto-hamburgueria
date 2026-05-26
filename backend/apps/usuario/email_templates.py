def renderizar_template_email(nome, codigo, titulo_contexto, texto_contexto):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #121212;
                margin: 0;
                padding: 40px 0;
                color: #ffffff;
            }}
            .container {{
                max-width: 500px;
                background-color: #1e1e1e;
                margin: 0 auto;
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                border: 1px solid #2d2d2d;
            }}
            .logo-text {{
                font-size: 26px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 5px;
            }}
            .logo-dot {{
                color: #ff6b00;
            }}
            .divider {{
                height: 2px;
                background: linear-gradient(to right, transparent, #ff6b00, transparent);
                margin: 20px 0;
            }}
            h2 {{
                color: #ff6b00;
                font-size: 22px;
                margin-top: 0;
            }}
            p {{
                font-size: 15px;
                color: #b3b3b3;
                line-height: 1.6;
            }}
            .code-box {{
                background-color: #2a2a2a;
                border: 2px dashed #ff6b00;
                display: inline-block;
                padding: 12px 30px;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 5px;
                color: #ffffff;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .footer {{
                font-size: 12px;
                color: #666666;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-text">Code <span class="logo-dot">•</span> Burger</div>
            <div class="divider"></div>
            <h2>{titulo_contexto}</h2>
            <p>Olá, <strong>{nome}</strong>!</p>
            <p>{texto_contexto}</p>
            <div class="code-box">{codigo}</div>
            <p>Insira esse código na tela do aplicativo para prosseguir.</p>
            <div class="footer">
                &copy; 2026 Code Burger - Hamburgueria Virtual. Todos os direitos reservados.
            </div>
        </div>
    </body>
    </html>
    """
