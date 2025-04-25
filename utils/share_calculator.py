# utils/share_calculator.py

def calculate_share(laba_bersih, porsi_a, porsi_b):
    total_porsi = porsi_a + porsi_b
    if total_porsi == 0:
        return {
            'laba_bersih': laba_bersih,
            'porsi_a': porsi_a,
            'porsi_b': porsi_b,
            'bagian_a': 0,
            'bagian_b': 0
        }

    bagian_a = (porsi_a / total_porsi) * laba_bersih
    bagian_b = (porsi_b / total_porsi) * laba_bersih

    return {
        'laba_bersih': laba_bersih,
        'porsi_a': porsi_a,
        'porsi_b': porsi_b,
        'bagian_a': bagian_a,
        'bagian_b': bagian_b
    }