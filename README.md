# Prevision-Engine
Etec de Hortolândia - PTCC - Informática para a Internet 2026

O Prevision Engine é uma API focada na organização e orientação na área de armazenamento de estoque que auxilia o funcionário a manusear seu sistema baseado na data da validade de seus produtos, sazonalidade e com o envio automatico de uma requisição para o reabastecimento do produto, fazendo com que nunca falte em seu estoque. Utilizando uma extensão que baixa uma demasiada quantidade de repositórios somada a IA integrada do Gemini, buscamos aperfeiçoar esse código cada vez mais em prol de tornarmos algo eficaz direcionado as empresas, e como consequência, chamar sua atenção pra que eventualmente esse projeto entre como um produto de mercado benéfico para as grandes industrias que possuem significancia.

Clonar o repositório
git clone https://github.com/yugi657/Prevision-Engine/tree/main/Prevision-Engine

cd prevision-engine

(Opcional) Criar ambiente virtual para isolamento

python -m venv venv

source venv/bin/activate  # No Windows: venv\Scripts\activate

Instalar dependências
pip install -r requirements.txt

Configurar variáveis de ambiente (Crucial)
Defina no seu SO: GEMINI_API_KEY, PREVISION_EMAIL_USER, PREVISION_EMAIL_PASSWORD
