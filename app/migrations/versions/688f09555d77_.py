"""empty message

Revision ID: 688f09555d77
Revises: 
Create Date: 2024-11-12 21:58:47.347338

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "688f09555d77"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Apprenti",
        sa.Column("id_apprenti", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nom", sa.String(length=50), nullable=False),
        sa.Column("prenom", sa.String(length=50), nullable=False),
        sa.Column("login", sa.String(length=50), nullable=False),
        sa.Column("mdp", sa.Text(), nullable=True),
        sa.Column("photo", sa.String(length=100), nullable=True),
        sa.Column("essais", sa.Integer(), nullable=False),
        sa.Column("archive", sa.Boolean(), nullable=False),
        sa.Column("adaptation_situation_examen", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_apprenti"),
        schema="main",
    )
    op.create_table(
        "ElementBase",
        sa.Column("id_element", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("libelle", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("text", sa.String(length=50), nullable=True),
        sa.Column("audio", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id_element"),
        schema="main",
    )
    op.create_table(
        "Formation",
        sa.Column("id_formation", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("intitule", sa.String(length=50), nullable=False),
        sa.Column("niveau_qualif", sa.Integer(), nullable=True),
        sa.Column("groupe", sa.String(length=50), nullable=True),
        sa.Column("image", sa.String(length=100), nullable=True),
        sa.Column("archive", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id_formation"),
        schema="main",
    )
    op.create_table(
        "Materiel",
        sa.Column("id_materiel", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nom", sa.String(length=50), nullable=False),
        sa.Column("categorie", sa.String(length=50), nullable=False),
        sa.Column("lien", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id_materiel"),
        schema="main",
    )
    op.create_table(
        "Personnel",
        sa.Column("id_personnel", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nom", sa.String(length=50), nullable=False),
        sa.Column("prenom", sa.String(length=50), nullable=False),
        sa.Column("login", sa.String(length=50), nullable=False),
        sa.Column("mdp", sa.Text(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("essais", sa.Integer(), nullable=False),
        sa.Column("archive", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id_personnel"),
        schema="main",
    )
    op.create_table(
        "Pictogramme",
        sa.Column("id_pictogramme", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("label", sa.String(length=50), nullable=False),
        sa.Column("url", sa.String(length=100), nullable=False),
        sa.Column("categorie", sa.String(length=50), nullable=False),
        sa.Column("souscategorie", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id_pictogramme"),
        schema="main",
    )
    op.create_table(
        "Cours",
        sa.Column("id_cours", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("theme", sa.String(length=50), nullable=False),
        sa.Column("cours", sa.String(length=50), nullable=False),
        sa.Column("duree", sa.Integer(), nullable=True),
        sa.Column("archive", sa.Boolean(), nullable=False),
        sa.Column("id_formation", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_formation"],
            ["main.Formation.id_formation"],
        ),
        sa.PrimaryKeyConstraint("id_cours"),
        schema="main",
    )
    with op.batch_alter_table("Cours", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_main_Cours_id_formation"), ["id_formation"], unique=False)

    op.create_table(
        "EducAdmin",
        sa.Column("id_personnel", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_personnel"],
            ["main.Personnel.id_personnel"],
        ),
        sa.PrimaryKeyConstraint("id_personnel"),
        schema="main",
    )
    op.create_table(
        "Assister",
        sa.Column("id_apprenti", sa.Integer(), nullable=False),
        sa.Column("id_cours", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_apprenti"],
            ["main.Apprenti.id_apprenti"],
        ),
        sa.ForeignKeyConstraint(
            ["id_cours"],
            ["main.Cours.id_cours"],
        ),
        sa.PrimaryKeyConstraint("id_apprenti", "id_cours"),
        schema="main",
    )
    op.create_table(
        "FicheIntervention",
        sa.Column("id_fiche", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("nom_du_demandeur", sa.String(length=50), nullable=True),
        sa.Column("date_demande", sa.Date(), nullable=True),
        sa.Column("localisation", sa.String(length=50), nullable=True),
        sa.Column("description_demande", sa.Text(), nullable=True),
        sa.Column("degre_urgence", sa.Integer(), nullable=True),
        sa.Column("couleur_intervention", sa.String(length=50), nullable=True),
        sa.Column("etat_fiche", sa.Integer(), nullable=True),
        sa.Column("date_creation", sa.DateTime(), nullable=True),
        sa.Column("photo_avant", sa.String(length=150), nullable=True),
        sa.Column("photo_apres", sa.String(length=150), nullable=True),
        sa.Column("nom_intervenant", sa.String(length=50), nullable=False),
        sa.Column("prenom_intervenant", sa.String(length=50), nullable=False),
        sa.Column("id_apprenti", sa.Integer(), nullable=False),
        sa.Column("id_personnel", sa.Integer(), nullable=False),
        sa.Column("id_cours", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_apprenti"],
            ["main.Apprenti.id_apprenti"],
        ),
        sa.ForeignKeyConstraint(
            ["id_cours"],
            ["main.Cours.id_cours"],
        ),
        sa.ForeignKeyConstraint(
            ["id_personnel"],
            ["main.Personnel.id_personnel"],
        ),
        sa.PrimaryKeyConstraint("id_fiche"),
        schema="main",
    )
    with op.batch_alter_table("FicheIntervention", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_main_FicheIntervention_id_apprenti"), ["id_apprenti"], unique=False)
        batch_op.create_index(batch_op.f("ix_main_FicheIntervention_id_cours"), ["id_cours"], unique=False)
        batch_op.create_index(batch_op.f("ix_main_FicheIntervention_id_personnel"), ["id_personnel"], unique=False)

    op.create_table(
        "ComposerPresentation",
        sa.Column("id_element", sa.Integer(), nullable=False),
        sa.Column("id_fiche", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=50), nullable=True),
        sa.Column("taille_texte", sa.String(length=50), nullable=True),
        sa.Column("audio", sa.String(length=50), nullable=True),
        sa.Column("police", sa.String(length=50), nullable=True),
        sa.Column("couleur", sa.String(length=7), nullable=True),
        sa.Column("couleur_fond", sa.String(length=7), nullable=True),
        sa.Column("niveau", sa.Integer(), nullable=True),
        sa.Column("position_elem", sa.String(length=50), nullable=True),
        sa.Column("ordre_saisie_focus", sa.String(length=50), nullable=True),
        sa.Column("id_pictogramme", sa.Integer(), nullable=True),
        sa.Column("taille_pictogramme", sa.Integer(), nullable=True),
        sa.Column("couleur_pictogramme", sa.String(length=7), nullable=True),
        sa.Column("id_materiel", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_element"],
            ["main.ElementBase.id_element"],
        ),
        sa.ForeignKeyConstraint(
            ["id_fiche"],
            ["main.FicheIntervention.id_fiche"],
        ),
        sa.ForeignKeyConstraint(
            ["id_materiel"],
            ["main.Materiel.id_materiel"],
        ),
        sa.ForeignKeyConstraint(
            ["id_pictogramme"],
            ["main.Pictogramme.id_pictogramme"],
        ),
        sa.PrimaryKeyConstraint("id_element", "id_fiche"),
        schema="main",
    )
    with op.batch_alter_table("ComposerPresentation", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_main_ComposerPresentation_id_materiel"), ["id_materiel"], unique=False)
        batch_op.create_index(batch_op.f("ix_main_ComposerPresentation_id_pictogramme"), ["id_pictogramme"], unique=False)

    op.create_table(
        "LaisserTrace",
        sa.Column("id_personnel", sa.Integer(), nullable=False),
        sa.Column("horodatage", sa.DateTime(), nullable=False),
        sa.Column("intitule", sa.String(length=50), nullable=False),
        sa.Column("eval_texte", sa.Text(), nullable=False),
        sa.Column("commentaire_texte", sa.Text(), nullable=False),
        sa.Column("eval_audio", sa.String(length=255), nullable=True),
        sa.Column("commentaire_audio", sa.String(length=50), nullable=True),
        sa.Column("apprenti", sa.Integer(), nullable=True),
        sa.Column("id_fiche", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_fiche"],
            ["main.FicheIntervention.id_fiche"],
        ),
        sa.ForeignKeyConstraint(
            ["id_personnel"],
            ["main.Personnel.id_personnel"],
        ),
        sa.PrimaryKeyConstraint("id_personnel", "horodatage"),
        schema="main",
    )
    with op.batch_alter_table("LaisserTrace", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_main_LaisserTrace_id_fiche"), ["id_fiche"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("LaisserTrace", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_main_LaisserTrace_id_fiche"))

    op.drop_table("LaisserTrace", schema="main")
    with op.batch_alter_table("ComposerPresentation", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_main_ComposerPresentation_id_pictogramme"))
        batch_op.drop_index(batch_op.f("ix_main_ComposerPresentation_id_materiel"))

    op.drop_table("ComposerPresentation", schema="main")
    with op.batch_alter_table("FicheIntervention", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_main_FicheIntervention_id_personnel"))
        batch_op.drop_index(batch_op.f("ix_main_FicheIntervention_id_cours"))
        batch_op.drop_index(batch_op.f("ix_main_FicheIntervention_id_apprenti"))

    op.drop_table("FicheIntervention", schema="main")
    op.drop_table("Assister", schema="main")
    op.drop_table("EducAdmin", schema="main")
    with op.batch_alter_table("Cours", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_main_Cours_id_formation"))

    op.drop_table("Cours", schema="main")
    op.drop_table("Pictogramme", schema="main")
    op.drop_table("Personnel", schema="main")
    op.drop_table("Materiel", schema="main")
    op.drop_table("Formation", schema="main")
    op.drop_table("ElementBase", schema="main")
    op.drop_table("Apprenti", schema="main")
    # ### end Alembic commands ###
