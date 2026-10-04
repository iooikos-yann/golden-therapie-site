#!/usr/bin/env python3
"""Génère en/index.html et pt/index.html à partir de index.html (source FR).

Usage : python3 tools/i18n.py   (depuis la racine du dépôt)

Chaque entrée de TEXTS est remplacée uniquement sous une forme « délimitée »
(>texte<, 'texte' ou "texte") pour ne jamais toucher un fragment de mot.
RAW contient les fragments HTML qui ne rentrent pas dans ce moule.
Le script échoue si une chaîne FR n'est plus trouvée (texte modifié dans le design).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'

LANGS = {
    'fr': {'html': 'fr', 'dir': ''},
    'en': {'html': 'en', 'dir': 'en/'},
    'pt': {'html': 'pt-PT', 'dir': 'pt/'},
}

# (fr, en, pt)
TEXTS = [
    # Navigation / héros
    ('Kinésithérapie', 'Physiotherapy', 'Fisioterapia'),
    ('Esthétique avancée', 'Advanced aesthetics', 'Estética avançada'),
    ('Tarifs', 'Prices', 'Preços'),
    ('Équipe', 'Team', 'Equipa'),
    ('Contact', 'Contact', 'Contacto'),
    ('Notre flyer', 'Our flyer', 'O nosso folheto'),
    ('Massages', 'Massages', 'Massagens'),
    ('Des soins personnalisés pour votre santé et votre beauté.', 'Personalised care for your health and beauty.', 'Cuidados personalizados para a sua saúde e beleza.'),
    ('Pour une meilleure qualité de vie.', 'For a better quality of life.', 'Para uma melhor qualidade de vida.'),
    ('Galets alignés sur le sable', 'Pebbles lined up on sand', 'Seixos alinhados na areia'),
    # Kinésithérapie
    ('KINÉSITHÉRAPIE', 'PHYSIOTHERAPY', 'FISIOTERAPIA'),
    ('Dos et colonne vertébrale', 'Back and spine', 'Costas e coluna vertebral'),
    ('Retrouvez votre mobilité et votre bien-être grâce à une prise en charge personnalisée.', 'Regain your mobility and well-being with personalised care.', 'Recupere a sua mobilidade e o seu bem-estar graças a um acompanhamento personalizado.'),
    ('Nous prenons en charge', 'We treat', 'Tratamos'),
    ('Traitement personnalisé', 'Personalised treatment', 'Tratamento personalizado'),
    ('Techniques modernes', 'Modern techniques', 'Técnicas modernas'),
    ('Accompagnement professionnel', 'Professional support', 'Acompanhamento profissional'),
    ('Douleurs du dos et du cou', 'Back and neck pain', 'Dores nas costas e no pescoço'),
    ('Rééducation après chirurgie', 'Post-surgery rehabilitation', 'Reabilitação pós-cirúrgica'),
    ('Traumatologie et blessures sportives', 'Trauma and sports injuries', 'Traumatologia e lesões desportivas'),
    ('Tendinites et douleurs articulaires', 'Tendinitis and joint pain', 'Tendinites e dores articulares'),
    ('Rééducation neurologique', 'Neurological rehabilitation', 'Reabilitação neurológica'),
    ('Rééducation respiratoire', 'Respiratory rehabilitation', 'Reabilitação respiratória'),
    ('Drainage lymphatique', 'Lymphatic drainage', 'Drenagem linfática'),
    ('Rééducation périnéale', 'Pelvic floor rehabilitation', 'Reabilitação do pavimento pélvico'),
    # Performance
    ('Préparation physique avec haltères', 'Strength training with dumbbells', 'Preparação física com halteres'),
    ('Optimisez vos capacités et atteignez vos objectifs grâce à un accompagnement adapté et personnalisé.', 'Optimise your abilities and reach your goals with tailored, personalised support.', 'Otimize as suas capacidades e alcance os seus objetivos com um acompanhamento adaptado e personalizado.'),
    ('Préparation physique', 'Physical conditioning', 'Preparação física'),
    ('Programmes sur mesure pour améliorer force, endurance, mobilité et condition physique.', 'Tailored programmes to improve strength, endurance, mobility and fitness.', 'Programas à medida para melhorar a força, a resistência, a mobilidade e a condição física.'),
    ('Performance sportive', 'Sports performance', 'Desempenho desportivo'),
    ('Préparation spécifique pour sportifs et équipes.', 'Specific preparation for athletes and teams.', 'Preparação específica para atletas e equipas.'),
    ('Bilans et tests', 'Assessments and testing', 'Avaliações e testes'),
    ('Évaluation complète pour un suivi précis et efficace.', 'Comprehensive assessment for precise, effective follow-up.', 'Avaliação completa para um acompanhamento preciso e eficaz.'),
    ('Coaching personnalisé', 'Personal coaching', 'Coaching personalizado'),
    ('Accompagnement individuel et motivation pour des résultats durables.', 'One-to-one support and motivation for lasting results.', 'Acompanhamento individual e motivação para resultados duradouros.'),
    ('Performance · Récupération', 'Performance · Recovery', 'Performance · Recuperação'),
    ('Force · Mobilité · Endurance', 'Strength · Mobility · Endurance', 'Força · Mobilidade · Resistência'),
    ('Bien-être · Confiance · Résultats', 'Well-being · Confidence · Results', 'Bem-estar · Confiança · Resultados'),
    # Esthétique
    ('ESTHÉTIQUE AVANCÉE', 'ADVANCED AESTHETICS', 'ESTÉTICA AVANÇADA'),
    ("Prenez soin de vous avec des soins innovants et des massages bien-être pour révéler votre beauté naturelle et retrouver l'harmonie.", 'Treat yourself to innovative treatments and wellness massages that reveal your natural beauty and restore your balance.', 'Cuide de si com tratamentos inovadores e massagens de bem-estar para revelar a sua beleza natural e reencontrar a harmonia.'),
    ('Massages bien-être', 'Wellness massages', 'Massagens de bem-estar'),
    ('Soins visage', 'Facial treatments', 'Tratamentos de rosto'),
    ('Nettoyage profond, hydratation, anti-âge, éclat du teint.', 'Deep cleansing, hydration, anti-ageing, radiant complexion.', 'Limpeza profunda, hidratação, antienvelhecimento, luminosidade da pele.'),
    ('Soins corps', 'Body treatments', 'Tratamentos de corpo'),
    ('Soins amincissants, raffermissants, drainants et remodelants.', 'Slimming, firming, draining and body-contouring treatments.', 'Tratamentos de emagrecimento, reafirmantes, drenantes e modeladores.'),
    ('Épilation définitive', 'Permanent hair removal', 'Depilação definitiva'),
    ('Technologie laser pour une peau douce, nette et durable.', 'Laser technology for smooth, clean, long-lasting results.', 'Tecnologia laser para uma pele suave, limpa e duradoura.'),
    ('Massage relaxant', 'Relaxing massage', 'Massagem relaxante'),
    ('Détente profonde, réduction du stress.', 'Deep relaxation, stress relief.', 'Relaxamento profundo, redução do stress.'),
    ('Massage thérapeutique', 'Therapeutic massage', 'Massagem terapêutica'),
    ('Soulage les tensions et les douleurs musculaires.', 'Relieves tension and muscle pain.', 'Alivia as tensões e as dores musculares.'),
    ("Favorise la circulation et réduit la rétention d'eau.", 'Boosts circulation and reduces water retention.', 'Favorece a circulação e reduz a retenção de líquidos.'),
    ('Massage sportif', 'Sports massage', 'Massagem desportiva'),
    ("Prépare le corps à l'effort et favorise la récupération.", 'Prepares the body for exercise and aids recovery.', 'Prepara o corpo para o esforço e favorece a recuperação.'),
    # Tarifs — interface
    ('GRILLE TARIFAIRE', 'PRICE LIST', 'TABELA DE PREÇOS'),
    ("Le coût de toutes les consultations d'évaluation et de conseil pour l'ensemble des soins esthétiques sera déduit du montant total lors de l'achat d'un forfait.", 'The cost of all assessment and advice consultations for aesthetic treatments is deducted from the total when you purchase a package.', 'O valor de todas as consultas de avaliação e aconselhamento para tratamentos estéticos é deduzido do total na compra de um pack.'),
    ('Rechercher un soin : laser, sourcils, drainage…', 'Search a treatment: laser, brows, drainage…', 'Pesquisar um tratamento: laser, sobrancelhas, drenagem…'),
    ('Rechercher dans la grille tarifaire', 'Search the price list', 'Pesquisar na tabela de preços'),
    ('Effacer', 'Clear', 'Limpar'),
    ('Prestation', 'Treatment', 'Tratamento'),
    ('Durée', 'Duration', 'Duração'),
    ('Prix', 'Price', 'Preço'),
    ('1 soin trouvé', '1 treatment found', '1 tratamento encontrado'),
    # Tarifs — catégories et prestations
    ('Massage californien', 'Californian massage', 'Massagem californiana'),
    ('Massage soin géothermal', 'Geothermal massage treatment', 'Massagem geotermal'),
    ('Réflexologie plantaire', 'Foot reflexology', 'Reflexologia podal'),
    ('Massage aux bambous (localisé)', 'Bamboo massage (targeted)', 'Massagem com bambus (localizada)'),
    ('Massage aux bambous (corps entier)', 'Bamboo massage (full body)', 'Massagem com bambus (corpo inteiro)'),
    ('Massage aux bougies (localisé)', 'Candle massage (targeted)', 'Massagem com velas (localizada)'),
    ('Massage aux bougies (corps entier)', 'Candle massage (full body)', 'Massagem com velas (corpo inteiro)'),
    ('Massage chiropratique', 'Chiropractic massage', 'Massagem quiroprática'),
    ('Massage thérapeutique (localisé)', 'Therapeutic massage (targeted)', 'Massagem terapêutica (localizada)'),
    ('Massage modelant (localisé)', 'Body-sculpting massage (targeted)', 'Massagem modeladora (localizada)'),
    ('Drainage lymphatique (Vodder / Leduc)', 'Lymphatic drainage (Vodder / Leduc)', 'Drenagem linfática (Vodder / Leduc)'),
    ('Massage pré / post-sport', 'Pre / post-sport massage', 'Massagem pré / pós-desporto'),
    ('Massage express', 'Express massage', 'Massagem express'),
    ('Soin du visage', 'Facial care', 'Cuidados de rosto'),
    ('Consultation et recommandations', 'Consultation and recommendations', 'Consulta e recomendações'),
    ('Mini-soin du visage + diagnostic de la peau', 'Mini facial + skin diagnosis', 'Mini-tratamento de rosto + diagnóstico da pele'),
    ('Traitements / produits à domicile', 'Home treatments / products', 'Tratamentos / produtos para casa'),
    ('Nettoyage profond de la peau', 'Deep skin cleansing', 'Limpeza de pele profunda'),
    ("Réponse d'hydratation", 'Hydrating treatment', 'Tratamento de hidratação'),
    ('Réponse nutritionnelle', 'Nourishing treatment', 'Tratamento nutritivo'),
    ('Réponse purificatrice', 'Purifying treatment', 'Tratamento purificante'),
    ('Réponse apaisante', 'Soothing treatment', 'Tratamento calmante'),
    ('Soin visage anti-âge', 'Anti-ageing facial', 'Tratamento de rosto antienvelhecimento'),
    ('Soins correctifs', 'Corrective treatment', 'Tratamento corretivo'),
    ('Soins Global Lift', 'Global Lift treatment', 'Tratamento Global Lift'),
    ('Soins Eternal', 'Eternal treatment', 'Tratamento Eternal'),
    ('Soins Timeless Prodigy', 'Timeless Prodigy treatment', 'Tratamento Timeless Prodigy'),
    ('Soins Power Retinol', 'Power Retinol treatment', 'Tratamento Power Retinol'),
    ('Soins Dermapeel-Pro (peeling chimique)', 'Dermapeel-Pro treatment (chemical peel)', 'Tratamento Dermapeel-Pro (peeling químico)'),
    ('Massages spécifiques', 'Specialised massages', 'Massagens específicas'),
    ('Massage facial liftant japonais « Kobido »', 'Japanese lifting facial massage “Kobido”', 'Massagem facial lifting japonesa «Kobido»'),
    ('Protocole Gua Sha', 'Gua Sha protocol', 'Protocolo Gua Sha'),
    ('Technologies', 'Technologies', 'Tecnologias'),
    ('Massage par radiofréquence avec brassards', 'Radiofrequency massage with cuffs', 'Massagem por radiofrequência com braçadeiras'),
    ('Photothérapie (visage et corps)', 'Phototherapy (face and body)', 'Fototerapia (rosto e corpo)'),
    ('Soins du corps', 'Body treatments', 'Tratamentos de corpo'),
    ('Consultation', 'Consultation', 'Consulta'),
    ('Évaluation du corps + diagnostic', 'Body assessment + diagnosis', 'Avaliação corporal + diagnóstico'),
    ('Soins corporels (enveloppements / bandages)', 'Body treatments (wraps / bandages)', 'Tratamentos corporais (envolvimentos / ligaduras)'),
    ('Anti-cellulite / amincissant', 'Anti-cellulite / slimming', 'Anticelulite / emagrecimento'),
    ('Raffermissement / tonification', 'Firming / toning', 'Reafirmação / tonificação'),
    ('Exfoliation / détoxification', 'Exfoliation / detox', 'Esfoliação / desintoxicação'),
    ('Microneedling corps', 'Body microneedling', 'Microneedling corporal'),
    ('Session de pressothérapie', 'Pressotherapy session', 'Sessão de pressoterapia'),
    ('Épilation laser', 'Laser hair removal', 'Depilação a laser'),
    ('Femmes · par séance', 'Women · per session', 'Mulheres · por sessão'),
    ('Aisselles', 'Underarms', 'Axilas'),
    ('½ jambes', 'Half legs', 'Meia perna'),
    ('Jambes complètes', 'Full legs', 'Pernas completas'),
    ('Avant-bras', 'Forearms', 'Antebraços'),
    ('Bras', 'Arms', 'Braços'),
    ('Bras complets', 'Full arms', 'Braços completos'),
    ('Aine standard', 'Standard bikini line', 'Virilha normal'),
    ('Aine complète', 'Full bikini line', 'Virilha completa'),
    ('Abdomen', 'Abdomen', 'Abdómen'),
    ('Ligne blanche', 'Navel line', 'Linha alba'),
    ('Aréoles', 'Areolas', 'Aréolas'),
    ('Lèvre supérieure', 'Upper lip', 'Buço'),
    ('Sillon interfessier', 'Intergluteal area', 'Sulco interglúteo'),
    ('Menton', 'Chin', 'Queixo'),
    ('Cuisses', 'Thighs', 'Coxas'),
    ('Hommes · par séance', 'Men · per session', 'Homens · por sessão'),
    ('Abdomen seul', 'Abdomen only', 'Apenas abdómen'),
    ('Dos complet', 'Full back', 'Costas completas'),
    ('Épaules', 'Shoulders', 'Ombros'),
    ('Torse', 'Chest', 'Peito'),
    ('Nuque', 'Nape', 'Nuca'),
    ('Maillot standard', 'Standard bikini line', 'Virilha normal'),
    ('Zone lombaire seule', 'Lower back only', 'Apenas zona lombar'),
    ('Maillot intégral', 'Full Brazilian', 'Virilha integral'),
    ('Packs hommes', "Men's packages", 'Packs homem'),
    ('Torse + abdomen', 'Chest + abdomen', 'Peito + abdómen'),
    ('Aisselles + maillot standard', 'Underarms + standard bikini line', 'Axilas + virilha normal'),
    ('½ jambes + maillot standard', 'Half legs + standard bikini line', 'Meia perna + virilha normal'),
    ('Aisselles + lèvre supérieure', 'Underarms + upper lip', 'Axilas + buço'),
    ('Jambes complètes + maillot intégral', 'Full legs + full Brazilian', 'Pernas completas + virilha integral'),
    ('Menton + lèvre supérieure', 'Chin + upper lip', 'Queixo + buço'),
    ('Épaules + dos complet', 'Shoulders + full back', 'Ombros + costas completas'),
    ('Épilation au fil', 'Threading', 'Depilação com linha'),
    ('Dessin de sourcils + épilation', 'Eyebrow shaping + threading', 'Design de sobrancelhas + depilação'),
    ('Lèvre supérieure (à partir de)', 'Upper lip (from)', 'Buço (desde)'),
    ('Visage & favoris, sans sourcils (à partir de)', 'Face & sideburns, excl. brows (from)', 'Rosto e patilhas, sem sobrancelhas (desde)'),
    ('Front', 'Forehead', 'Testa'),
    ('Sourcils & pigmentation', 'Brows & pigmentation', 'Sobrancelhas e pigmentação'),
    ('Sourcils poil par poil (à partir de)', 'Hair-stroke brows (from)', 'Sobrancelhas fio a fio (desde)'),
    ('Retouche après un mois (à partir de)', 'Touch-up after one month (from)', 'Retoque após um mês (desde)'),
    ('Sourcils ombrés (à partir de)', 'Powder brows (from)', 'Sobrancelhas sombreadas (desde)'),
    ('Micropigmentation', 'Micropigmentation', 'Micropigmentação'),
    ('Eye-liner supérieur (à partir de)', 'Upper eyeliner (from)', 'Eyeliner superior (desde)'),
    ('Eye-liner inférieur (à partir de)', 'Lower eyeliner (from)', 'Eyeliner inferior (desde)'),
    ('Correction des lèvres (à partir de)', 'Lip correction (from)', 'Correção de lábios (desde)'),
    ('Maquillage complet des lèvres (à partir de)', 'Full lip colour (from)', 'Maquilhagem completa dos lábios (desde)'),
    ('Micropigmentation paramédicale', 'Paramedical micropigmentation', 'Micropigmentação paramédica'),
    ('Cuir chevelu', 'Scalp', 'Couro cabeludo'),
    ('Aréole du sein', 'Breast areola', 'Aréola mamária'),
    ("Cicatrices d'implants", 'Implant scars', 'Cicatrizes de implantes'),
    ('Extensions de cils', 'Eyelash extensions', 'Extensões de pestanas'),
    ('Cils classiques', 'Classic lashes', 'Pestanas clássicas'),
    ('1re application', 'First application', 'Primeira aplicação'),
    ('Entretien 2 semaines', '2-week refill', 'Manutenção 2 semanas'),
    ('Entretien 3 semaines', '3-week refill', 'Manutenção 3 semanas'),
    ('Volume russe', 'Russian volume', 'Volume russo'),
    ('Pédicure médicale', 'Medical pedicure', 'Pedicure médica'),
    ('Séance laser', 'Laser session', 'Sessão de laser'),
    ('Pied diabétique', 'Diabetic foot', 'Pé diabético'),
    ('Engelures et fissures', 'Chilblains and cracked skin', 'Frieiras e fissuras'),
    ('Traitement à la paraffine chaude', 'Hot paraffin treatment', 'Tratamento com parafina quente'),
    # Équipe
    ('Des professionnels passionnés à votre écoute pour vous accompagner vers votre bien-être.', 'Passionate professionals who listen and guide you towards well-being.', 'Profissionais apaixonados, atentos a si, para o acompanhar rumo ao bem-estar.'),
    ('Écoute et bienveillance', 'Attentive, caring approach', 'Escuta e empatia'),
    ('Soins personnalisés', 'Personalised care', 'Cuidados personalizados'),
    ('Expertise et expérience', 'Expertise and experience', 'Competência e experiência'),
    ('Accompagnement sur le long terme', 'Long-term support', 'Acompanhamento a longo prazo'),
    ('Votre bien-être, notre engagement.', 'Your well-being, our commitment.', 'O seu bem-estar, o nosso compromisso.'),
    ("L'équipe Golden Therapie", 'The Golden Therapie team', 'A equipa Golden Therapie'),
    # Contact
    ('Contactez-nous', 'Contact us', 'Contacte-nos'),
    ('Téléphone', 'Phone', 'Telefone'),
    ('Mobile', 'Mobile', 'Telemóvel'),
    ('E-mail', 'Email', 'E-mail'),
    ('Suivez-nous et restez informés !', 'Follow us and stay up to date!', 'Siga-nos e mantenha-se informado!'),
    ('Télécharger notre flyer (PDF)', 'Download our flyer (PDF)', 'Descarregar o nosso folheto (PDF)'),
    ('Kinésithérapie, performance, massages et esthétique avancée à Strassen, Luxembourg.', 'Physiotherapy, performance, massages and advanced aesthetics in Strassen, Luxembourg.', 'Fisioterapia, performance, massagens e estética avançada em Strassen, Luxemburgo.'),
]

# Fragments HTML / JS bruts (fr, en, pt)
RAW = [
    ('>Votre <span', '>Your <span', '>O seu <span'),
    ('>bien-être</span>', '>well-being</span>', '>bem-estar</span>'),
    ('>commence ici.</span>', '>starts here.</span>', '>começa aqui.</span>'),
    ('>Prévenir <span', '>Prevent <span', '>Prevenir <span'),
    ('</span> Traiter <span', '</span> Treat <span', '</span> Tratar <span'),
    ('</span> Accompagner</p>', '</span> Support</p>', '</span> Acompanhar</p>'),
    ('>Prévenir • Traiter • Accompagner<', '>Prevent • Treat • Support<', '>Prevenir • Tratar • Acompanhar<'),
    ('>Notre <span', '>Our <span', '>A nossa <span'),
    ('>équipe</span>', '>team</span>', '>equipa</span>'),
    ('>Aucun soin ne correspond à « {{ q }} ».<', '>No treatment matches “{{ q }}”.<', '>Nenhum tratamento corresponde a «{{ q }}».<'),
    ('`${count} soins trouvés`', '`${count} treatments found`', '`${count} tratamentos encontrados`'),
]

LANG_SWITCH = re.compile(r'<!--lang-->.*?<!--/lang-->', re.S)


def lang_switch(cur):
    up = '../' if LANGS[cur]['dir'] else ''
    links = []
    for code, cfg in LANGS.items():
        href = (up + cfg['dir']) or './'
        if code == cur:
            links.append(f'<a href="{href}" aria-current="page" style="color:#a8661a;font-weight:500">{code.upper()}</a>')
        else:
            links.append(f'<a href="{href}" hreflang="{cfg["html"]}">{code.upper()}</a>')
    return ('<!--lang--><span style="display:inline-flex;gap:12px;padding-left:clamp(14px,2vw,28px);'
            'border-left:1px solid rgba(14,35,71,.18)">' + ''.join(links) + '</span><!--/lang-->')


def translate(html, idx):
    missing = []
    for row in RAW:
        if row[0] not in html:
            missing.append(row[0])
        html = html.replace(row[0], row[idx])
    # plus longues d'abord : « Bras complets » avant « Bras »
    for row in sorted(TEXTS, key=lambda r: -len(r[0])):
        fr, out = row[0], row[idx]
        hit = False
        for l, r in (('>', '<'), ("'", "'"), ('"', '"')):
            needle = l + fr + r
            if needle in html:
                hit = True
                repl = out
                if l == "'" and "'" in out:  # chaîne JS : bascule en guillemets doubles
                    html = html.replace(needle, '"' + out + '"')
                    continue
                html = html.replace(needle, l + repl + r)
        if not hit:
            missing.append(fr)
    return html, missing


def main():
    src = SRC.read_text(encoding='utf-8')
    if '<!--lang-->' not in src:
        sys.exit('marqueur <!--lang--> absent de index.html')
    SRC.write_text(LANG_SWITCH.sub(lang_switch('fr'), src), encoding='utf-8')
    for idx, code in ((1, 'en'), (2, 'pt')):
        html, missing = translate(src, idx)
        if missing:
            sys.exit(f'[{code}] chaînes FR introuvables (design modifié ?) :\n  ' + '\n  '.join(missing))
        html = html.replace('<html lang="fr">', f'<html lang="{LANGS[code]["html"]}">', 1)
        html = (html.replace('src="assets/', 'src="../assets/')
                    .replace('href="assets/', 'href="../assets/')
                    .replace('url(fonts/', 'url(../fonts/')
                    .replace('src="./support.js"', 'src="../support.js"'))
        html = LANG_SWITCH.sub(lang_switch(code), html)
        out = ROOT / code / 'index.html'
        out.parent.mkdir(exist_ok=True)
        out.write_text(html, encoding='utf-8')
        print(f'ok {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
