import os
import smtplib
import logging
import json
import time  # NOVA LINHA: Necessária para o tempo de espera entre tentativas (Retries)
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
    # MUDANÇA: Adicionado o parâmetro 'dry_run' com o padrão Falso (desativado)
    def __init__(self, api_key: str, dry_run: bool = False):
        self.client = genai.Client(api_key=api_key)
        self.remetente = os.getenv("PREVISION_EMAIL_USER")
        self.senha = os.getenv("PREVISION_EMAIL_PASSWORD")
        self.dry_run = dry_run  # NOVA LINHA: Guarda o estado do modo de simulação
        logging.info(f"Motor Prevision v1.1 inicializado. Modo Dry-Run (Simulação): {self.dry_run}")

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

    # MUDANÇA: O método agora retorna um DataFrame contendo o relatório de auditoria
    def analisar_e_agir(self, df: pd.DataFrame) -> pd.DataFrame:
        
        # --- MELHORIA 1: VALIDAÇÃO DEFENSIVA (FAIL-FAST) ---
        colunas_obrigatorias = ['id_produto', 'nome', 'email_fornecedor']
        for col in colunas_obrigatorias:
            if col not in df.columns:
                logging.critical(f"Erro de Validação: A coluna obrigatória '{col}' não foi encontrada na tabela.")
                raise ValueError(f"A tabela fornecida precisa conter a coluna: '{col}'")
        
        prompt = f"Analise o inventário (Mês 12). Dados: {df.to_json(orient='records')}"
        response = None
        
        # --- MELHORIA 2: MECANISMO DE TENTATIVAS (RETRIES) ---
        max_tentativas = 3
        for tentativa in range(1, max_tentativas + 1):
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
                break  # Se a chamada funcionou, quebra o loop de tentativas e segue em frente
            except Exception as e:
                logging.warning(f"Tentativa {tentativa}/{max_tentativas} falhou ao conectar com o Gemini: {e}")
                if tentativa < max_tentativas:
                    time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
                else:
                    logging.critical("Todas as tentativas de comunicação com a IA falharam.")
                    raise e
        
        # --- MELHORIA 3: GERAÇÃO DE HISTÓRICO (AUDITORIA) ---
        dados_auditoria = []  # Lista temporária para salvar as decisões
        
        try:
            decisoes = json.loads(response.text)['analise_produtos']
            
            for d in decisoes:
                item = df[df['id_produto'] == d['id_produto']].iloc[0]
                logging.info(f"SKU {d['id_produto']} ({item['nome']}): {d['acao']}")
                
                # Registra a decisão da IA no nosso dicionário de auditoria
                registro = {
                    "id_produto": d['id_produto'],
                    "nome_produto": item['nome'],
                    "acao_proposta": d['acao'],
                    "quantidade": d['quantidade_comprar'],
                    "justificativa": d['justificativa'],
                    "email_enviado": False  # Padrão é falso, muda se o e-mail sair de fato
                }
                
                if d['acao'] == 'COMPRAR' and d['quantidade_comprar'] > 0:
                    # --- MELHORIA 4: TRAVA DE SEGURANÇA (DRY-RUN) ---
                    if self.dry_run:
                        logging.info(f"⚠️ [DRY-RUN] Ordem de compra SIMULADA para {item['nome']} ({d['quantidade_comprar']} un). Nenhum e-mail foi enviado.")
                    else:
                        self._disparar_email(item['email_fornecedor'], item['nome'], d['quantidade_comprar'])
                        registro["email_enviado"] = True  # Confirma o envio no relatório
                
                dados_auditoria.append(registro)  # Salva o registro na lista
                
        except Exception as e:
            logging.critical(f"Falha no processamento pós-inferência: {e}")
            raise e

        # Retorna o relatório final transformado em uma tabela do Pandas
        return pd.DataFrame(dados_auditoria)

# --- Fluxo de execução ---
if __name__ == "__main__":
    # Exemplo de uso ativando o modo Dry-Run para testes seguros:
    app = PrevisionEngine(api_key=os.getenv("GEMINI_API_KEY", ""), dry_run=True)
    
    # Criando uma tabela fictícia para demonstrar o funcionamento
    dados_teste = {
        'id_produto': [101, 102],
        'nome': ['Parafuso Alen', 'Chave de Fenda X'],
        'email_fornecedor': ['fornecedorA@email.com', 'fornecedorB@email.com']
    }
    df_inventario = pd.DataFrame(dados_teste)
    
    # Executando o sistema e capturando a tabela de auditoria devolvida por ele
    # relatorio_auditoria = app.analisar_e_agir(df_inventario)
    # print(relatorio_auditoria)
