import os
import smtplib
import logging
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import pandas as pd
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class DecisaoProduto(BaseModel):
    id_produto: int
    acao: str = Field(description="Ação: 'COMPRAR', 'PROMOÇÃO', ou 'MANTER'")
    quantidade_comprar: int = Field(default=0)
    justificativa: str = Field(description="Análise técnica baseada em dados.")

class RespostaIA(BaseModel):
    analise_produtos: List[DecisaoProduto]

class PrevisionEngine:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.remetente = os.getenv("PREVISION_EMAIL_USER")
        self.senha = os.getenv("PREVISION_EMAIL_PASSWORD")
        logging.info("Motor Prevision v1.0-RC inicializado com sucesso.")

    def _disparar_email(self, email_fornecedor: str, nome: str, qtd: int):
        if not self.remetente or not self.senha:
            logging.warning(f"SMTP não configurado. Simulação: {qtd}x {nome} para {email_fornecedor}")
            return
        
        msg = MIMEMultipart()
        msg['From'], msg['To'] = self.remetente, email_fornecedor
        msg['Subject'] = f"Ordem de Compra: {nome}"
        corpo = f"Prezado, solicitamos a reposição de {qtd} unidades de {nome}."
        msg.attach(MIMEText(corpo, 'plain'))

        try:
            with smtplib.SMTP(os.getenv("PREVISION_SMTP_SERVER", "smtp.gmail.com"), 587) as server:
                server.starttls()
                server.login(self.remetente, self.senha)
                server.sendmail(self.remetente, email_fornecedor, msg.as_string())
            logging.info(f"📧 E-mail disparado para {email_fornecedor}")
        except Exception as e:
            logging.error(f"Erro SMTP: {e}")

    def analisar_e_agir(self, df: pd.DataFrame):
        prompt = f"Analise o inventário (Mês 12). Dados: {df.to_json(orient='records')}"
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RespostaIA,
                    temperature=0.1
                )
            )
            decisoes = json.loads(response.text)['analise_produtos']
            
            for d in decisoes:
                item = df[df['id_produto'] == d['id_produto']].iloc[0]
                logging.info(f"SKU {d['id_produto']} ({item['nome']}): {d['acao']}")
                
                if d['acao'] == 'COMPRAR' and d['quantidade_comprar'] > 0:
                    self._disparar_email(item['email_fornecedor'], item['nome'], d['quantidade_comprar'])
        
        except Exception as e:
            logging.critical(f"Falha no processamento: {e}")

# --- Fluxo de execução ---
if __name__ == "__main__":
    app = PrevisionEngine(api_key=os.getenv("GEMINI_API_KEY", ""))
    # Carregue aqui seu DataFrame de produção