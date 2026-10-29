"""Programa 5: análisis de datos con Machine Learning (scikit-learn).
Predice el puntaje general de regulación de mercado (PMR) de 2023 de cada país
a partir de sus indicadores de 2018 (así no se usa el mismo año con el que se
calcula el puntaje), y agrupa países con KMeans."""
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Cargar datos limpios (salida de limpieza.py)
df = pd.read_csv("indicadores_limpio.csv")

# 2. Tabla país-año x indicador (solo indicadores sin desglose)
base = df[df["COMP_BREAKDOWN_1"] == "_Z"]
tabla = base.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns="INDICATOR", values="OBS_VALUE")
print("Tabla país-año x indicador:", tabla.shape)

# 3. Variable a predecir: PMR 2023. Variables de entrada: indicadores de 2018
y = tabla.xs(2023, level="TIME_PERIOD")["PTY_MR_PMR"]
X = tabla.xs(2018, level="TIME_PERIOD").drop(columns=["PTY_MR_PMR"])
paises = X.index.intersection(y.index)
X, y = X.loc[paises], y.loc[paises]
X = pd.DataFrame(SimpleImputer(strategy="median").fit_transform(X), columns=X.columns, index=X.index)
print("Países con datos en 2018 y 2023:", len(X))

# 4. División entrenamiento / prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 5. Entrenar y evaluar dos modelos
modelos = {
    "Regresión Ridge": Ridge(alpha=1.0),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
}
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    cv = cross_val_score(modelo, X, y, cv=5, scoring="r2")
    print(f"\n{nombre}")
    print(f"  R2 (prueba):        {r2_score(y_test, pred):.3f}")
    print(f"  MAE:                {mean_absolute_error(y_test, pred):.3f}")
    print(f"  RMSE:               {mean_squared_error(y_test, pred) ** 0.5:.3f}")
    print(f"  R2 validación (5):  {cv.mean():.3f} +/- {cv.std():.3f}")

# 6. Importancia de variables del Random Forest
rf = modelos["Random Forest"]
imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nIndicadores de 2018 más importantes para predecir el PMR 2023:")
print(imp.head(5).round(3))

# 7. Agrupar países en 3 grupos con KMeans (indicadores de 2023)
x23 = tabla.xs(2023, level="TIME_PERIOD").drop(columns=["PTY_MR_PMR"])
x23 = pd.DataFrame(SimpleImputer(strategy="median").fit_transform(x23), columns=x23.columns, index=x23.index)
esc = StandardScaler().fit_transform(x23)
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(esc)
grupos = pd.DataFrame({"pais": x23.index, "grupo": km.labels_,
                       "PMR": tabla.xs(2023, level="TIME_PERIOD").loc[x23.index, "PTY_MR_PMR"].values})
print("\nPMR promedio por grupo (2023):")
print(grupos.groupby("grupo")["PMR"].agg(["count", "mean"]).round(2))
for g in sorted(grupos["grupo"].unique()):
    print(f"Grupo {g}:", ", ".join(grupos[grupos["grupo"] == g]["pais"]))
