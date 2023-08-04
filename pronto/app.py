from flask import Flask, render_template, request

app = Flask(__name__)

# Lista de produtos (inicialmente vazia)
estoque = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        produto = request.form["produto"]
        quantidade = int(request.form["quantidade"])
        operacao = request.form["operacao"]

        if operacao == "entrada":
            estoque.append((produto, quantidade))
        elif operacao == "saida":
            for i, (prod, qtd) in enumerate(estoque):
                if prod == produto:
                    estoque[i] = (prod, qtd - quantidade)
                    break

    return render_template("index.html", estoque=estoque)

if __name__ == "__main__":
    app.run(debug=True)
