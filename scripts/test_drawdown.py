from app.analytics.drawdown import DrawdownAnalyzer

equity = [

    100000,

    101000,

    103000,

    98000,

    96000,

    99000,

    104000,

    102000,

]

result = DrawdownAnalyzer.analyze(equity)

for k, v in result.items():
    print(f"{k:25}: {v}")