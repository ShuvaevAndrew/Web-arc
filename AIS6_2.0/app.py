from flask import Flask, render_template
from auth_service import auth_blueprint
from table_service import table_blueprint
from record_service import record_blueprint

app = Flask(__name__)

def register_blueprints():
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(table_blueprint)
    app.register_blueprint(record_blueprint)

register_blueprints()

@app.route('/table/<table_name>')
def view_table(table_name):
    return render_template('table.html', table_name=table_name, records=[], editing_enabled=False)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
