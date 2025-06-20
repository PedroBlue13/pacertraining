market_sections = {
    "Fresh Produce": ["Fruits", "Vegetables", "Herbs"],
    "Bakery": ["Fresh Bread", "Cakes", "Pastries"],
    "Beverages": ["Juices", "Soft Drinks", "Coffee", "Beer"],
    "Cleaning & Household": ["Detergents", "Paper Goods", "Kitchen Essentials"]
}


formulas = {
    "Markup_simples": [
        "preco_venda = custo_produto × (1 + markup_percentual)"
    ],
    "Markup_inverso": [
        "preco_venda = custo_produto / (1 - margem_desejada)"
    ],
    "Markup_sobre_custos_totais": [
        "preco_venda = (custos_fixos + custos_variaveis + despesas) × (1 + markup_percentual)"
    ],
    "Markup_dinamico": [
        "preco_venda = custo_produto × fator_dinamico",
        "# onde fator_dinamico varia conforme estoque, demanda, sazonalidade etc."
    ],
    "Markup_competitivo": [
        "preco_venda = preco_medio_mercado ± ajuste_percentual",
        "# usado quando se baseia nos concorrentes"
    ],
    "Markup_financeiro_completo": [
        "preco_venda = custo_produto / (1 - (despesas_fixas + despesas_variaveis + Margem_lucro))"
    ],
    "Margem_contribuicao": [
        "Margem_contribuicao = preco_venda - (custos_variaveis + despesas_variaveis)"
    ],
    "Venda_margem_de_lucro_bjetiva": [
        "preco_venda = custos_produto / (1 - taxas_de_venda - margem_objetiva)"
    ],
    "Precificacao_baseada_concorrencia": [
        "preco_venda = preco_concorrente ± ajuste_percentual"
    ],
    "Precificacao_valor_percebido": [
        "preco_venda = valor_percebido_pelo_cliente - desconto_estrategico"
    ]
}


section_pricing_strategies = {
    "Fresh Produce": ["Precificacao_baseada_concorrencia", "Markup"],
    "Bakery": ["Markup", "Venda_margem_de_lucro_bjetiva", "Precificacao_valor_percebido"],
    "Beverages": ["Precificacao_baseada_concorrencia", "Markup", "Margem_contribuicao"],
    "Cleaning & Household": ["Precificacao_baseada_concorrencia", "Markup", "Margem_contribuicao"]
}



"""
Markup_simples: Útil para produtos de baixo custo e venda recorrente
O que é: Aplica um percentual fixo sobre o custo do produto para obter o preço de venda. É rápido e fácil, mas pode não considerar todas as despesas indiretas.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Markup_inverso: Ideal para quando se conhece o preço final desejado e quer calcular o custo máximo aceitável
O que é: Calcula o preço de venda com base no custo e na margem de lucro desejada, considerando a margem como uma fração do preço final.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Markup_sobre_custos_totais: Recomendado para negócios que incluem todos os custos (fixos e variáveis) no preço final
O que é: Soma todos os custos envolvidos no produto e aplica um markup sobre esse total, garantindo que despesas e lucros estejam cobertos.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Markup_dinamico: Indicado para mercados sazonais ou com demanda variável
O que é: O fator de markup varia conforme critérios como estoque, sazonalidade, urgência de venda ou comportamento do consumidor.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Markup_competitivo: Estratégia útil em mercados com muita concorrência e preços transparentes
O que é: Define o preço com base no valor praticado pelos concorrentes, ajustando conforme o posicionamento da marca.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Markup_financeiro_completo: Ideal para precificação detalhada com despesas fixas, variáveis e margem de lucro
O que é: Método mais robusto de markup, que calcula o preço considerando todos os custos e a margem desejada, muito usado em planilhas empresariais.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Margem_contribuicao: Importante para analisar a lucratividade de cada produto e otimizar a gestão de custos
O que é: Indica quanto cada produto contribui para cobrir os custos fixos e gerar lucro. Muito útil para tomada de decisão e mix de produtos.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Venda_margem_de_lucro_bjetiva: Ideal para produtos com custos variáveis e margem de lucro definida
O que é: Define o preço com base nos custos, taxas e na margem de lucro desejada. Boa escolha para empresas que buscam controle financeiro rigoroso.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Precificacao_baseada_concorrencia: Indicada para mercados competitivos, onde a comparação de preços é comum
O que é: Analisar os preços praticados pelos concorrentes e definir um preço similar ou ligeiramente diferente, dependendo do posicionamento da marca e diferenciais do produto.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Precificacao_valor_percebido: Ideal para produtos com alto valor agregado e diferenciais competitivos
O que é: Define o preço com base no valor que o cliente percebe no produto ou serviço, considerando diferenciais como exclusividade, qualidade, experiência de uso, etc.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
