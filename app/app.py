import db
import logging
from flask import abort, render_template, Flask
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS Espacos FROM ESPACO').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS Promotores FROM PROMOTOR').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS Atividades FROM ATIVIDADE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS Regioes FROM REGIAO').fetchone()
    stats.update(x)
    logging.info(stats)
    return render_template('index.html', stats=stats)

# --------------------------------------------------------

# Espacos page
@APP.route('/espacos/')
def list_espacos():
    espacos = db.execute(
    '''
    SELECT EspacoId, Nome, Tipo, Lotacao, Morada, RegiaoId
    FROM ESPACO
    ORDER BY EspacoId
    ''').fetchall()
    return render_template('espaco-list.html', espacos=espacos)


@APP.route('/espacos/<int:id>/')
def get_espaco(id):
    espaco = db.execute(
    '''
    SELECT EspacoId, Nome, Tipo, Lotacao, Morada, RegiaoId
    FROM ESPACO
    WHERE EspacoId = %s
    ''', id).fetchone()

    if espaco is None:
        abort(404, f'Espaço {id} não existe')

    # atividades que o espaco pode acolher
    atividades = db.execute(
        '''
        SELECT AtividadeId, ATIVIDADE.Nome AS Nome
        FROM (ESPACO NATURAL JOIN ESPACO_ATIVIDADE) JOIN ATIVIDADE USING (AtividadeId)
        WHERE EspacoId = %s
        ''', id
    ).fetchall()

    return render_template('espaco.html', espaco=espaco, atividades=atividades)

@APP.route('/espacos/pesquisa/<expr>/')
def search_espaco(expr):
    search = { 'expr': expr }
    expr = '%' + expr + '%'
    espacos = db.execute(
      ''' 
      SELECT EspacoId, Nome
      FROM ESPACO 
      WHERE Nome LIKE %s
      ORDER BY Nome
      ''', expr).fetchall()
    return render_template('espaco-pesquisa.html', search=search, espacos=espacos)

@APP.route('/espacos/pesquisa_avancada_distrito/<distrito>/')
def distrito_espaco(distrito):
    search = { 'expr':distrito}
    distrito = '%' + distrito + '%'
    espaco=db.execute(
        '''
        SELECT EspacoId, Nome
        FROM ESPACO NATURAL JOIN REGIAO
        WHERE REGIAO.Distrito LIKE %s
        ORDER BY Nome
        ''', distrito).fetchall()
    return render_template('espaco-pesquisa.html', search=search,espacos=espaco)

@APP.route('/espacos/pesquisa_avancada_nutsiii/<nutsiii>/')
def nutsiii_espaco(nutsiii):
    search = { 'expr':nutsiii}
    nutsiii = '%' + nutsiii + '%'
    espacos=db.execute(
        '''
        SELECT EspacoId, Nome
        FROM ESPACO NATURAL JOIN REGIAO
        WHERE REGIAO.NUTS_III LIKE %s
        ORDER BY Nome
        ''', nutsiii).fetchall()
    return render_template('espaco-pesquisa.html', search=search,espacos=espacos)

@APP.route('/espacos/pesquisa_avancada_nutsii/<nutsii>/')
def nutsii_espacos(nutsii):
    search = { 'expr':nutsii}
    nutsii = '%' + nutsii + '%'
    espacos=db.execute(
        '''
        SELECT EspacoId, Nome
        FROM ESPACO NATURAL JOIN REGIAO NATURAL JOIN NUTS
        WHERE NUTS.NUTS_II LIKE %s
        ORDER BY Nome
        ''', nutsii).fetchall()
    return render_template('espaco-pesquisa.html', search=search,espacos=espacos)

@APP.route('/espacos/pesquisa_avancada_atividade/<atividades>/')
def atividades_espacos(atividades):
    search = { 'expr':atividades}
    atividades = '%' + atividades + '%'
    espacos=db.execute(
        '''
        SELECT EspacoId, Nome 
        FROM ESPACO
        WHERE EspacoId IN 
            (SELECT EspacoId FROM ESPACO_ATIVIDADE NATURAL JOIN ATIVIDADE WHERE ATIVIDADE.Nome LIKE %s)
        ''', atividades).fetchall()
    return render_template('espaco-pesquisa.html', search=search,espacos=espacos)

# --------------------------------------------------------

# Promotores
@APP.route('/promotores/')
def list_promotores():
    promotores = db.execute(
    '''
    SELECT PromotorId, Nome, Morada, CodPostal, RegiaoId
    FROM PROMOTOR
    ORDER BY Nome
    ''').fetchall()
    return render_template('promotor-list.html', promotores=promotores)


@APP.route('/promotores/<int:id>/')
def get_promotor(id):
    promotor = db.execute(
    '''
    SELECT PromotorId, Nome, Morada, CodPostal, RegiaoId
    FROM PROMOTOR
    WHERE PromotorId = %s
    ''', id).fetchone()

    if promotor is None:
        abort(404, f'Promotor {id} não existe')
    
    # tipo de atividades que o pomotor pode promover
    atividades = db.execute(
        '''
        SELECT AtividadeId, ATIVIDADE.Nome AS Nome
        FROM (PROMOTOR NATURAL JOIN PROMOTOR_ATIVIDADE) JOIN ATIVIDADE USING (AtividadeId)
        WHERE PromotorId = %s
        ''', id
    ).fetchall()

    return render_template('promotor.html', promotor=promotor, atividades=atividades)

@APP.route('/promotores/pesquisa/<expr>/')
def search_promotor(expr):
    search = { 'expr': expr }
    expr = '%' + expr + '%'
    promotores = db.execute(
      ''' 
      SELECT PromotorId, Nome
      FROM PROMOTOR 
      WHERE Nome LIKE %s
      ORDER BY Nome
      ''', expr).fetchall()
    return render_template('promotor-pesquisa.html', search=search, promotores=promotores)

@APP.route('/promotores/pesquisa_avancada_distrito/<distrito>/')
def distrito_promotor(distrito):
    search = { 'expr':distrito}
    distrito = '%' + distrito + '%'
    promotores=db.execute(
        '''
        SELECT PromotorId, Nome
        FROM PROMOTOR NATURAL JOIN REGIAO
        WHERE REGIAO.Distrito LIKE %s
        ORDER BY Nome
        ''', distrito).fetchall()
    return render_template('promotor-pesquisa.html', search=search,promotores=promotores)

@APP.route('/promotores/pesquisa_avancada_nutsiii/<nutsiii>/')
def nutsiii_promotor(nutsiii):
    search = { 'expr':nutsiii}
    nutsiii = '%' + nutsiii + '%'
    promotores=db.execute(
        '''
        SELECT PromotorId, Nome
        FROM PROMOTOR NATURAL JOIN REGIAO
        WHERE REGIAO.NUTS_III LIKE %s
        ORDER BY Nome
        ''', nutsiii).fetchall()
    return render_template('promotor-pesquisa.html', search=search,promotores=promotores)

@APP.route('/promotores/pesquisa_avancada_nutsii/<nutsii>/')
def nutsii_promotor(nutsii):
    search = { 'expr':nutsii}
    nutsii = '%' + nutsii + '%'
    promotores=db.execute(
        '''
        SELECT PromotorId, Nome
        FROM PROMOTOR NATURAL JOIN REGIAO NATURAL JOIN NUTS
        WHERE NUTS.NUTS_II LIKE %s
        ORDER BY Nome
        ''', nutsii).fetchall()
    return render_template('promotor-pesquisa.html', search=search,promotores=promotores)

@APP.route('/promotores/pesquisa_avancada_atividade/<atividades>/')
def atividades_promotor(atividades):
    search = { 'expr':atividades}
    atividades = '%' + atividades + '%'
    promotores=db.execute(
        '''
        SELECT PromotorId,Nome 
        FROM PROMOTOR 
        WHERE PromotorId IN 
            (SELECT PromotorId FROM PROMOTOR_ATIVIDADE NATURAL JOIN ATIVIDADE WHERE ATIVIDADE.Nome LIKE %s)
        ''', atividades).fetchall()
    return render_template('promotor-pesquisa.html', search=search,promotores=promotores)

# --------------------------------------------------------

@APP.route('/promotores/pesquisa_avancada/')
def adv_search_promotor():
    return render_template('promotor-adv-search.html')

@APP.route('/espacos/pesquisa_avancada/')
def adv_search_espaco():
    return render_template('espaco-adv-search.html')

# --------------------------------------------------------

# Regioes page
@APP.route('/regioes/')
def list_regioes():
    regioes = db.execute(
    '''
    SELECT RegiaoId, Distrito, NUTS_III
    FROM REGIAO
    ORDER BY RegiaoId
    ''').fetchall()
    return render_template('regiao-list.html', regioes=regioes)

@APP.route('/regioes/<int:id>')
def get_regiao(id):
    regiao = db.execute(
    '''
    SELECT RegiaoId, Distrito, NUTS_III
    FROM REGIAO
    WHERE RegiaoId = %s
    ''', id).fetchone()

    if regiao is None:
        abort(404, f'Regiao {id} não existe')

    return render_template('regiao.html', regiao=regiao)

# --------------------------------------------------------

# NUTS page
@APP.route('/nuts/')
def list_nuts():
    nuts = db.execute(
    '''
    SELECT NUTS_III, NUTS_II, NUTS_I
    FROM NUTS
    ORDER BY NUTS_I, NUTS_II, NUTS_II
    ''').fetchall()
    return render_template('nuts-list.html', nuts=nuts)

@APP.route('/nuts/<nutsiii>')
def get_nuts(nutsiii):
    nuts = db.execute(
    '''
    SELECT NUTS_III, NUTS_II, NUTS_I
    FROM NUTS
    WHERE NUTS_III LIKE %s
    ''', nutsiii).fetchone()

    if nuts is None:
        abort(404, f'NUTS III "{id}" não existe')

    return render_template('nuts.html', nuts=nuts)

#----------------------------------------------------------

# Para as páginas de pesquisa de espaços para um dado promotor
@APP.route('/espacos-para-promotor-distrito/<int:id>')
def espaco_para_promotor_distrito(id):
    search = db.execute(
        '''
        SELECT Nome
        FROM PROMOTOR
        WHERE PromotorId = %s
        ''', id
    ). fetchone()

    if (search is None):
        abort(404, f'Promotor {id} não existe')
    
    dicionario=db.execute(
        '''
        SELECT ESPACO.EspacoId, ESPACO.Nome AS espNome, ATIVIDADE.Nome AS atvNome
        FROM ESPACO JOIN ESPACO_ATIVIDADE ON (ESPACO.EspacoId=ESPACO_ATIVIDADE.EspacoId)
                    JOIN ATIVIDADE ON (ATIVIDADE.AtividadeId=ESPACO_ATIVIDADE.AtividadeId) 
        WHERE
        ESPACO.EspacoId IN (
            SELECT ESPACO.EspacoId 
            FROM ESPACO NATURAL JOIN REGIAO 
            WHERE REGIAO.Distrito IN (
                SELECT REGIAO.Distrito 
                FROM PROMOTOR NATURAL JOIN REGIAO 
                WHERE PROMOTOR.PromotorId = %s
            )
        ) 
        AND
        ATIVIDADE.Nome IN (
            SELECT ATIVIDADE.Nome 
            FROM (ATIVIDADE NATURAL JOIN PROMOTOR_ATIVIDADE) JOIN PROMOTOR USING (PromotorId)
            WHERE PROMOTOR.PromotorId = %s
        )
        ORDER BY EspacoId;
        ''', [id, id]).fetchall()
    return render_template('espacos-para-promotor.html',search=search,dicionario=dicionario)

@APP.route('/espacos-para-promotor-nutsiii/<int:id>')
def espaco_para_promotor_nutsiii(id):
    search = db.execute(
        '''
        SELECT Nome
        FROM PROMOTOR
        WHERE PromotorId = %s
        ''', id
    ). fetchone()

    if (search is None):
        abort(404, f'Promotor {id} não existe')

    dicionario=db.execute(
        '''
        SELECT ESPACO.EspacoId, ESPACO.Nome AS espNome, ATIVIDADE.Nome AS atvNome
        FROM ESPACO JOIN ESPACO_ATIVIDADE ON (ESPACO.EspacoId=ESPACO_ATIVIDADE.EspacoId)
                    JOIN ATIVIDADE ON (ATIVIDADE.AtividadeId=ESPACO_ATIVIDADE.AtividadeId) 
        WHERE
        ESPACO.EspacoId IN (
            SELECT ESPACO.EspacoId 
            FROM ESPACO NATURAL JOIN REGIAO 
            WHERE REGIAO.NUTS_III IN (
                SELECT REGIAO.NUTS_III 
                FROM PROMOTOR NATURAL JOIN REGIAO 
                WHERE PROMOTOR.PromotorId = %s
            )
        ) 
        AND 
        ATIVIDADE.Nome IN (
            SELECT ATIVIDADE.Nome 
            FROM (ATIVIDADE NATURAL JOIN PROMOTOR_ATIVIDADE) JOIN PROMOTOR USING (PromotorId)
            WHERE PROMOTOR.PromotorId = %s
        )
        ORDER BY EspacoId;
        ''', [id, id]).fetchall()
    return render_template('espacos-para-promotor.html',search=search,dicionario=dicionario)

# --------------------------------------------------------

# Para as páginas onde é dado o número de espaços e promotoras por atividade por distrito
@APP.route('/regioes/pesquisa_agrupada_espacos/')
def list_agrupada_espaco():
    distritos = db.execute(
        '''
        SELECT DISTINCT Distrito
        FROM REGIAO
        ORDER BY Distrito
        '''
    ).fetchall()

    agrupada = db.execute(
    '''
    SELECT REGIAO.Distrito AS Distrito, ATIVIDADE.Nome AS Atividade, COUNT(ESPACO.EspacoId) AS NumEspacos
    FROM (REGIAO JOIN ATIVIDADE)
         LEFT OUTER JOIN
         (ESPACO NATURAL JOIN ESPACO_ATIVIDADE)
         ON (ESPACO.RegiaoId=REGIAO.RegiaoId AND ESPACO_ATIVIDADE.AtividadeId=ATIVIDADE.AtividadeId)
    GROUP BY REGIAO.Distrito, ATIVIDADE.Nome 
    ORDER BY REGIAO.Distrito, ATIVIDADE.Nome;
    ''').fetchall()
    return render_template('agrupada-espacos-list.html',distritos=distritos, agrupada=agrupada)


@APP.route('/regioes/pesquisa_agrupada_promotores/')
def list_agrupada_promotor():
    distritos = db.execute(
        '''
        SELECT DISTINCT Distrito
        FROM REGIAO
        ORDER BY Distrito
        '''
    ).fetchall()

    agrupada = db.execute(
    '''
    SELECT REGIAO.Distrito AS Distrito, ATIVIDADE.Nome AS Atividade, COUNT(PROMOTOR.PromotorId) AS NumPromotores
    FROM (REGIAO JOIN ATIVIDADE)
         LEFT OUTER JOIN
         (PROMOTOR NATURAL JOIN PROMOTOR_ATIVIDADE)
         ON (PROMOTOR.RegiaoId=REGIAO.RegiaoId AND PROMOTOR_ATIVIDADE.AtividadeId=ATIVIDADE.AtividadeId)
    GROUP BY REGIAO.Distrito, ATIVIDADE.Nome 
    ORDER BY REGIAO.Distrito, ATIVIDADE.Nome;
    ''').fetchall()
    return render_template('agrupada-promotores-list.html', distritos=distritos, agrupada=agrupada)

# --------------------------------------------------------

# atividades page
@APP.route('/atividades/')
def list_atividades():
    atividades = db.execute(
        '''
        SELECT AtividadeId, Nome
        FROM ATIVIDADE
        ORDER BY AtividadeId
        '''
    ).fetchall()
    return render_template('atividade-list.html', atividades=atividades)

@APP.route('/atividades/<int:id>')
def get_atividade(id):
    atividade = db.execute(
    '''
    SELECT AtividadeId, Nome
    FROM ATIVIDADE
    WHERE AtividadeId = %s
    ''', id).fetchone()

    if atividade is None:
        abort(404, f'Atividade {id} não existe')    

    return render_template('atividade.html', atividade=atividade)

@APP.route('/espacos-para-atividade/<int:id>')
def get_espacos_atividade(id):
    atividade = db.execute(
    '''
    SELECT AtividadeId, Nome
    FROM ATIVIDADE
    WHERE AtividadeId = %s
    ''', id).fetchone()

    espacos = db.execute(
        '''
            SELECT EspacoId, ESPACO.Nome AS Nome
            FROM (ESPACO NATURAL JOIN ESPACO_ATIVIDADE) JOIN ATIVIDADE USING (AtividadeId)
            WHERE AtividadeId = %s
        ''', id
    ).fetchall()

    return render_template('atividade-espacos.html', atividade=atividade, espacos=espacos)

@APP.route('/promotores-para-atividade/<int:id>')
def get_promotores_atividade(id):
    atividade = db.execute(
    '''
    SELECT AtividadeId, Nome
    FROM ATIVIDADE
    WHERE AtividadeId = %s
    ''', id).fetchone()

    promotores = db.execute(
        '''
            SELECT PromotorId, PROMOTOR.Nome AS Nome
            FROM (PROMOTOR NATURAL JOIN PROMOTOR_ATIVIDADE) JOIN ATIVIDADE USING (AtividadeId)
            WHERE AtividadeId = %s
        ''', id
    ).fetchall()

    return render_template('atividade-promotores.html', atividade=atividade, promotores=promotores)
