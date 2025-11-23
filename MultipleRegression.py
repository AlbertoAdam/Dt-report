import pandas as pd
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore")


def run_sleep_regression(filepath='sleep_data.csv'):
    """
    Runs a multiple regression model to predict sleep_score based on key sleep metrics.
    """
    try:
        df = pd.read_csv(filepath)

        # 1. Define the variables for the model
        # Dependent variable (what we want to predict)
        dependent_var = 'sleep_score'

        # Independent variables (what we use to predict)
        independent_vars = [
            'total_sleep_time',
            'deepsleepduration',
            'remsleepduration',
            'waso'  # Wake After Sleep Onset
        ]

        model_columns = [dependent_var] + independent_vars

        # 2. Prepare the data
        # Drop rows where any of our model's columns have missing data (NaN)
        df_model = df[model_columns].dropna()

        if df_model.empty:
            print(f"Error: After removing missing values, no data is left.")
            print(f"Original shape: {df.shape}. Check your CSV file for empty columns.")
            return

        # 3. Define X (independent) and Y (dependent)
        Y = df_model[dependent_var]
        X = df_model[independent_vars]

        # 4. Add a constant (intercept) to the model
        # statsmodels requires manually adding the intercept (b0 in y = b0 + b1*x1 + ...)
        X_with_const = sm.add_constant(X)

        # 5. Build and Fit the Ordinary Least Squares (OLS) model
        model = sm.OLS(Y, X_with_const).fit()

        # 6. Print the comprehensive model summary
        print("--- Multiple Regression Model Summary ---")
        print(f"Dependent Variable: {dependent_var}")
        print(f"Independent Variables: {', '.join(independent_vars)}\n")

        # The summary() method provides R-squared, coefficients, p-values, and more
        print(model.summary())

        # 7. Get predictions and display comparison
        print("\n--- Actual vs. Predicted Values ---")
        predictions = model.predict(X_with_const)

        # Create a DataFrame for comparison
        # Y (actual values) and predictions should share the same index from df_model
        df_comparison = pd.DataFrame({
            'Actual_Sleep_Score': Y,
            'Predicted_Sleep_Score': predictions
        })

        # Add a column for the difference (residual)
        df_comparison['Difference (Residual)'] = df_comparison['Actual_Sleep_Score'] - df_comparison[
            'Predicted_Sleep_Score']

        # Round the values for cleaner output
        df_comparison = df_comparison.round(2)

        # Print the comparison DataFrame
        # Use pd.options to make sure it prints well, showing all rows
        with pd.option_context('display.max_rows', None, 'display.width', 1000):
            print(df_comparison)

        # 8. Print Interpretation Guide
        print("\n--- Interpretation Guide ---")
        print(f"R-squared (R²): \tIndicates how much of the variance in '{dependent_var}' is explained by the model.")
        print(
            f"coef (Coefficient): \tThe estimated change in '{dependent_var}' for a one-unit increase in the variable, holding others constant.")
        print(
            f"P>|t| (p-value): \tLow values (e.g., < 0.05) suggest the variable is statistically significant in predicting '{dependent_var}'.")

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except KeyError as e:
        print(f"Error: A required column is missing from the CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Assuming 'sleep_data.csv' is in the same directory
    run_sleep_regression('sleep_data.csv')