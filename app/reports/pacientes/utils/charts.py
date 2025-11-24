# app/reports/pacientes/utils/charts.py

from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class ChartsGenerator:
    """
    Genera gráficos en memoria (BytesIO) para ser incrustados en el PDF.
    Todos los métodos devuelven un BytesIO con una imagen PNG.
    """

    def _empty_chart(self, title: str) -> BytesIO:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Sin datos disponibles", ha="center", va="center")
        ax.set_title(title)
        ax.axis("off")

        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="PNG")
        plt.close(fig)
        buf.seek(0)
        return buf

    def grafico_pacientes_nuevos_por_mes(self, df: pd.DataFrame) -> BytesIO:
        if df.empty:
            return self._empty_chart("Pacientes nuevos por mes")

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(data=df, x="mes", y="cantidad", ax=ax)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Pacientes nuevos")
        ax.set_title("Pacientes nuevos por mes")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="PNG")
        plt.close(fig)
        buf.seek(0)
        return buf

    def grafico_ranking_pacientes(self, df: pd.DataFrame) -> BytesIO:
        if df.empty:
            return self._empty_chart("Ranking de pacientes por consultas")

        # Orden descendente por cantidad
        df_sorted = df.sort_values("consultas", ascending=True)

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(
            data=df_sorted,
            x="consultas",
            y="paciente",
            ax=ax,
        )
        ax.set_xlabel("Consultas")
        ax.set_ylabel("Paciente")
        ax.set_title("Top pacientes por cantidad de consultas")

        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="PNG")
        plt.close(fig)
        buf.seek(0)
        return buf

    def grafico_pacientes_inactivos(self, df: pd.DataFrame) -> BytesIO:
        if df.empty:
            return self._empty_chart("Pacientes inactivos")

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(
            data=df.sort_values("dias_desde_ultima_consulta", ascending=False),
            x="dias_desde_ultima_consulta",
            y="paciente",
            ax=ax,
        )
        ax.set_xlabel("Días desde la última consulta")
        ax.set_ylabel("Paciente")
        ax.set_title("Pacientes más inactivos")

        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="PNG")
        plt.close(fig)
        buf.seek(0)
        return buf
