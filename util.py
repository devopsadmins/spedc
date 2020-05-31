from os import listdir
from os.path import isfile, join

__CODEC_PADRAO__ = 'iso8859-1'


def ler_diretorio_txt(diretorio='efd-c'):
    _lst_txt = []
    for txt in listdir(diretorio):
        if txt[-3:].upper() == 'TXT' and isfile(join(diretorio, txt)):
            _lst_txt.append(join(diretorio, txt))
    return _lst_txt


def f_monta_hirarquia_efd_c(hirarquia='hirarquia_efd_c.txt', nivel=True):
    """ Niveis_EFD-C """
    __dic_nivel_efd_c = {}
    cont = 0
    with open(hirarquia, 'r', encoding=__CODEC_PADRAO__) as arquivo_txt:
        for Linha in arquivo_txt:
            linha_quebrada = Linha.split('|')
            cont += 1
            if cont == 1:
                __dic_nivel_efd_c['id'] = {}
                __dic_nivel_efd_c['id'] = linha_quebrada
            else:
                linha_quebrada[1] = int(linha_quebrada[1]) if nivel else converte_para_valor(linha_quebrada[1])
                __dic_nivel_efd_c[linha_quebrada[0]] = {}
                __dic_nivel_efd_c[linha_quebrada[0]] = linha_quebrada

    return __dic_nivel_efd_c


def converte_para_valor(valor, qtd_decimais=2):
    valor = str(valor).rstrip().lstrip()
    valor = valor.replace(',', '.').replace("'", "")
    if valor in ('', 0, '-', '0', '.', None, 'None'):
        return 0
    else:
        try:
            valor = round(float(valor), qtd_decimais)
        except (ValueError, TypeError):
            pass
        return valor


def mapear_efd_c(txt, dic_nivel):
    _dic_efd_c = {}
    lst_filtro_am = []
    lst_filtro_ibge = []
    lst_n = [0, 0, 0, 0, 0, 0]
    lst_np = ['', '', '', '', '', '']

    with open(txt, 'r', encoding=__CODEC_PADRAO__) as open_arquivo_txt:
        numero_linha = 0

        for Linha in open_arquivo_txt:
            numero_linha += 1
            Linha = Linha.replace('\x96', '').replace('\x90', '').replace('…', '')


            ls = Linha.upper().split('|')
            reg = ls[1]

            if reg in dic_nivel:
                na = dic_nivel[reg][1]

            if numero_linha == 1:
                cnpj_ent, data_ref = ls[9], ls[6] + ls[7]
                data_ref = data_ref[-4:] + '_' + data_ref[:4][-2:]

                cnpj_data_ref = cnpj_ent + '|' + data_ref

            lst_n[na] = numero_linha
            lst_np[na] = ls[1]

            id_pai = lst_n[na - 1]
            reg_pai = lst_np[na - 1]

            if cnpj_data_ref not in _dic_efd_c:
                _dic_efd_c[cnpj_data_ref] = {}

                for chv_p in ('COD_ITEM', 'COD_PART'):
                    _dic_efd_c[cnpj_data_ref][chv_p] = {}

            if reg not in _dic_efd_c[cnpj_data_ref]:
                _dic_efd_c[cnpj_data_ref][reg] = {}

            if numero_linha not in _dic_efd_c[cnpj_data_ref][reg]:
                _dic_efd_c[cnpj_data_ref][reg][numero_linha] = {}
                _dic_efd_c[cnpj_data_ref][reg][numero_linha]['R'] = {}
                _dic_efd_c[cnpj_data_ref][reg][numero_linha]['F'] = {}

            if reg == 'C990':
                break

            if reg == '0140':
                ent = ls[4]


            if reg == '0150':
                ls[2] = str(ls[2]).rstrip().lstrip()
                if ls[8][:2] in ["13","14","15"]:
                    lst_filtro_ibge.append(ls[2])
                if ent not in _dic_efd_c[cnpj_data_ref]['COD_PART']:
                    _dic_efd_c[cnpj_data_ref]['COD_PART'][ent] = {}
                _dic_efd_c[cnpj_data_ref]['COD_PART'][ent][ls[2]] = ls

            # if reg == '0200':
            #     ls[2] = str(ls[2])
            #     if ent not in _dic_efd_c[cnpj_data_ref]['COD_ITEM']:
            #         _dic_efd_c[cnpj_data_ref]['COD_ITEM'][ent] = {}
            #     _dic_efd_c[cnpj_data_ref]['COD_ITEM'][ent][ls[2]] = ls

            ls[0] = id_pai
            _dic_efd_c[cnpj_data_ref][reg][numero_linha]['R'] = ls

            if numero_linha > 1:
                if reg not in _dic_efd_c[cnpj_data_ref][reg_pai][id_pai]['F']:
                    _dic_efd_c[cnpj_data_ref][reg_pai][id_pai]['F'][reg] = []
                _dic_efd_c[cnpj_data_ref][reg_pai][id_pai]['F'][reg].append(numero_linha)

    return _dic_efd_c, lst_filtro_am, lst_filtro_ibge
