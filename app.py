import os
import streamlit as st
from PyPDF2 import PdfMerger

# Configura o ícone e o título da página
st.set_page_config(page_title='Mesclador de PDFs', page_icon='🔗', layout='centered')
# O st.set_page_config deve ser chamado antes de qualquer outro comando do Streamlit no script.
# Isso porque ele configura a página do Streamlit e deve ser executado antes de qualquer componente ser renderizado na tela.

def mesclar_pdfs(arquivos_pdf):
    # Nome fixo do arquivo de saída
    nome_saida = 'mesclado.pdf'
    # Inicializa o objeto para mesclar PDFs
    mesclador = PdfMerger()
    for arquivo_pdf in arquivos_pdf:
        # Adiciona cada PDF à lista para mesclagem
        mesclador.append(arquivo_pdf)
    # Salva o arquivo mesclado
    mesclador.write(nome_saida)
    # Fecha o objeto
    mesclador.close()
    # Retorna o nome do arquivo gerado
    return nome_saida

# Título da aplicação
st.title('Mesclador de PDFs')

# Texto explicativo sobre o upload de PDFs
st.write('Faça upload de múltiplos PDFs para mesclá-los em um único arquivo.')

# Carregar arquivos PDF via upload
arquivos = st.file_uploader(
    'Selecione os arquivos PDF',
    type=['pdf'], # Restringe o tipo de arquivos permitidos
    accept_multiple_files=True, # Permite múltiplos arquivos
    help='Você pode carregar vários arquivos PDFs para mesclá-los.' # Mensagem de ajuda
)

# Botão para acionar a mesclagem
if st.button('Mesclar PDFs'):
    if arquivos: # Verifica se há arquivos carregados
        try:
            # Chama a função para mesclar os PDFs
            arquivo_saida = mesclar_pdfs(arquivos)

            # Mostra mensagem de sucesso e botão para download
            st.success(f'PDFs mesclados com sucesso! Arquivo gerado: {arquivo_saida}')
            # O uso de with open cuida automaticamente de fechar o arquivo após o bloco de código ser executado.
            # Isso é especialmente útil em aplicações de longo prazo, como servidores, pois evita o problema de "arquivos abertos"
            # que podem acumular recursos desnecessariamente.
            # Quando removemos o arquivo com os.remove, precisamos garantir que ele já foi totalmente lido e fechado.
            with open(arquivo_saida, 'rb') as arquivo:
                st.download_button(
                    label='Baixar PDF Mesclado', # Rótulo do botão de download
                    data=arquivo.read(), # Lê o conteúdo do arquivo gerado
                    file_name=arquivo_saida, # Nome do arquivo de saída
                    mime='application/pdf' # Tipo MIME para PDF
                )

            # Exclui o arquivo mesclado após disponibilizá-lo para download
            os.remove(arquivo_saida)
        except Exception as e: # Captura erros durante o processo
            st.error(f'Erro ao mesclar PDFs: {e}') # Exibe a mensagem de erro
    else:
        # Mensagem de aviso caso nenhum arquivo seja carregado
        st.warning('Por favor, carregue arquivos PDF para mesclar.')