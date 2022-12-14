def init_app(app):
    from .login import login_bp
    from .list import list_bp
    from .submit import submit_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(list_bp)
    app.register_blueprint(submit_bp)

    @app.after_request
    def _(response):
        if "Cache-Control" not in response.headers:
            for tp in ["image", "font", "css", "javascript"]:
                if tp in response.headers["Content-Type"]:
                    response.headers["Cache-Control"] = "public, max-age=2592000"
                    break
            else:
                response.headers["Cache-Control"] = "no-store"
        return response

    return app
