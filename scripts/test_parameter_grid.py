from app.optimization.parameter_grid import ParameterGrid


parameter_space = {
    "opening_candles": [3, 6, 9],
    "risk_reward": [1.5, 2],
}

grid = ParameterGrid.generate(parameter_space)

for params in grid:
    print(params)

print(f"\nTotal combinations: {len(grid)}")