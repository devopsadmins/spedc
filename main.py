from util import f_monta_hirarquia_efd_c
from util import ler_diretorio_txt
from util import ler_diretorio_txt_recursivo
from util import mapear_efd_c
import mysql.connector
import sys
import pandas as pd
from datetime import datetime
import itertools as it


def InserirDB():
    cnx = mysql.connector.connect(user='root', password='Comum_01',
                                  host='127.0.0.1',
                                  database='cbrs')
    mycursor = cnx.cursor()

    print(dict(it.islice(dic_xls, 1, 1000)))
    print("Gerado Dict: ", datetime.now() - start)

    # cnx.commit();
    # print("Numero:", mycursor.rowcount)


"""
pip install pandas
pip install openpyxl
"""
try:
    final = sys.argv[1]
except:
    final = "TESTE"

diretorio = "D:/freela/OneDrive - De Biasi Consultoria Tributária S S/CBRS/EFD-Contribuições/" + final + '/'
# diretorio = "./sped"
start = datetime.now()
print("Mapeando diretório com TXT: ", diretorio)
lst_txt_dir = ler_diretorio_txt_recursivo(diretorio)  # Diretório de leitura
dic_nivel_efd_c = f_monta_hirarquia_efd_c('hirarquia_efd_c.txt')  # arquivo de hierarquia - NÃO ALTERAR
dic_selic = f_monta_hirarquia_efd_c('selic.txt',
                                    False)  # Tabela SELIC para calculo de Juros - Atualizar no mes corrente via EXCEL
dic_ibge = f_monta_hirarquia_efd_c('ibge1.csv', False)  # tabela de estados IBGE

dic_xls = {}  # Saída de Dados
lst_cfop = ["5101", "5115", "1201", "5102", "5116", "1202", "5103", "5117", "1203", "5104", "5118", "1204", "5105",
            "5119", "1410", "5106", "5120", "1411", "5107", "5122", "5109", "5123", "5110", "5401", "5111", "5402",
            "5112", "5403", "5113", "5405", "5114"]  # filtro CFOP

"""
INDICE ZERO(0) SERÁ PAI DO REGISTRO
DIC[CNPJ_DATA_REF][REGISTRO][LINHA][R][LISTA DOS CAMPOS IGUAL EFD] - REGISTRO 
DIC[CNPJ_DATA_REF][REGISTRO][LINHA][F][REGISTRO FILHO][LISTA DE NUMEROS DE LINHAS DOS FILHOS] - FILHOS
"""
# 1635004
reg = 'C010'  # PARA FILTRAR O CNPJ DO AM
reg_filho = 'C100'
reg_neto = 'C170'  # FALTA FILTROS DO CFOP

for txt in lst_txt_dir:
    print("Lendo TXT:", txt)
    dic_efd_c = lst_filtro_am = lst_filtro_ibge = []
    linha = 0
    dic_efd_c, lst_filtro_am, lst_filtro_ibge = mapear_efd_c(txt, dic_nivel_efd_c)
    print("Tempo do Arquivo: ", datetime.now() - start)
    for cnpj_data_ref in dic_efd_c:
        cnpj, data_ref = cnpj_data_ref.split('|')
        if reg in dic_efd_c[cnpj_data_ref]:
            for id in dic_efd_c[cnpj_data_ref][reg]:
                cnpj_c010 = dic_efd_c[cnpj_data_ref][reg][id]['R'][2]

                # try:
                # para filtrar cnpj constante na tabela filtrada no "util.py" do AM
                if reg_filho in dic_efd_c[cnpj_data_ref][reg][id]['F']:
                    for id_filho in dic_efd_c[cnpj_data_ref][reg][id]['F'][reg_filho]:
                        indemit_c100 = dic_efd_c[cnpj_data_ref][reg_filho][id_filho]['R'][3]
                        codpart_c100 = dic_efd_c[cnpj_data_ref][reg_filho][id_filho]['R'][4]
                        nomepart = dic_efd_c[cnpj_data_ref]['COD_PART'][codpart_c100][3]
                        cnpjpart = dic_efd_c[cnpj_data_ref]['COD_PART'][codpart_c100][5]
                        cpfpart = dic_efd_c[cnpj_data_ref]['COD_PART'][codpart_c100][6]
                        cod_munic_part = dic_efd_c[cnpj_data_ref]['COD_PART'][codpart_c100][8]
                        if indemit_c100 == '0' and codpart_c100 in lst_filtro_ibge:

                            for id_neto in dic_efd_c[cnpj_data_ref][reg_filho][id_filho]['F'][reg_neto]:
                                ls = dic_efd_c[cnpj_data_ref][reg_neto][id_neto]['R']
                                cfop = ls[3]
                                # checa lista de CFOP e faz os calculos
                                if cfop in lst_cfop:
                                    try:
                                        produto = dic_efd_c[cnpj_data_ref]['COD_ITEM'][cnpj][ls[0]]
                                    except:
                                        produto = []

                                    # para criar a estrutura de saída
                                    cvh = cnpj_data_ref + "_" + cnpj_c010
                                    # if cvh not in dic_xls:
                                    #     dic_xls[0] = [cnpj_data_ref, cnpj_c010, data_ref, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    #                   0, 0, 0,
                                    #                   0, 0, 0, 0]
                                    dic_xls[linha] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                                    i = 0
                                    """
                                                0 cod_item 3
                                               1 descr_compl 4
                                               2 vl_item 7
                                               3 cfop 11

                                               4 cst_pis 25
                                               5 vl_bc_pis 26
                                               6 aliq_pis 27
                                               7 quant_bc_pis 28
                                               8 vl_pis 30

                                               9 cst_cofins 31
                                               10 vl_bc_cofins 32
                                               11 aliq_cofins 33
                                               12 quant_bc_cofins 34
                                               13 vl_cofins 36
                                               """
                                    dic_xls[linha][0] = cnpj_data_ref
                                    dic_xls[linha][1] = cnpj_c010
                                    dic_xls[linha][2] = data_ref
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = ls[i]
                                    i += 1
                                    dic_xls[linha][i + 3] = produto[3]
                                    i += 1
                                    dic_xls[linha][i + 3] = produto[7]
                                    i += 1
                                    dic_xls[linha][i + 3] = produto[8]
                                    i += 1
                                    linha += 1
                                    sql = "INSERT INTO `cbrs`.`cbrs` (`CHV`, `CNPJ_C010`, `DATA`, `cod_item`, `desc_item`, `vl_item`, `CFOP`, `CST_PIS`, `VL_BC_PIS`, `ALIQ_PIS`, `QUANT_BC_PIS`, `VL_PIS`, `CST_COFINS`, `VL_BC_COFINS`, `ALI_COFINS`, `QUANT_BC_COFINS`, `VL_CONFIS`, `DESC_0200`, `TIOPO_ITEM`, `COD_NCM`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    InserirDB()

    #
    # except:
    #     print("Erro: ", sys.exc_info()[0],sys.exc_info()[3])

    dic_efd_c.clear()
    filename = "".join(["./relatorio-", data_ref, "-", final, ".xlsx"])
    data = pd.DataFrame.from_dict(dic_xls, orient='index',
                                  columns=["CHV", "CNPJ_C010", "DATA", "cod_item", "desc_item", "vl_item", "CFOP",
                                           "CST_PIS", "VL_BC_PIS", "ALIQ_PIS", "QUANT_BC_PIS", "VL_PIS", "CST_COFINS",
                                           "VL_BC_COFINS", "ALI_COFINS", "QUANT_BC_COFINS", 'VL_CONFIS', "DESC_0200",
                                           'TIOPO_ITEM', 'COD_NCM'])

    data.to_excel(filename)
    print("Tempo do Arquivo: ", datetime.now() - start)

# filename = "./relatorio.xlsx"
# data = pd.DataFrame.from_dict(dic_xls, orient='index',
#                               columns=['0', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2',
#                                        '2',
#                                        '2', '2'])
# data.to_csv(filename)

print("Tempo total de processamento: ", datetime.now() - start)
print('fim')
