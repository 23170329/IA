public class Puzzle24 {
    private static final int SIZE = 5;

    public static String[] generarSucesores(String estadoActual) {
        String[] sucesores = new String[4];
        String[] piezas = estadoActual.split(",");
        int indice = -1;

        for (int i = 0; i < piezas.length; i++) {
            if (piezas[i].equals("0")) {
                indice = i;
                break;
            }
        }

        int fila = indice / SIZE;
        int col = indice % SIZE;
        int count = 0;

        // Movimientos: Arriba (-5), Abajo (+5), Izquierda (-1), Derecha (+1)
        int[] movs = {-SIZE, SIZE, -1, 1};

        for (int m : movs) {
            int destino = indice + m;
            if (destino >= 0 && destino < 25) {
                if (Math.abs(m) == 1 && (destino / SIZE != fila)) continue;

                String[] copia = piezas.clone();
                copia[indice] = copia[destino];
                copia[destino] = "0";
                sucesores[count++] = String.join(",", copia);
            }
        }
        return sucesores;
    }

    // Manhattan
    public static int calcularManhattan(String estado, String objetivo) {
        int dist = 0;
        String[] actual = estado.split(",");
        String[] obj = objetivo.split(",");
        for (int i = 0; i < 25; i++) {
            if (actual[i].equals("0")) continue;
            for (int j = 0; j < 25; j++) {
                if (actual[i].equals(obj[j])) {
                    dist += Math.abs(i / SIZE - j / SIZE) + Math.abs(i % SIZE - j % SIZE);
                    break;
                }
            }
        }
        return dist;
    }

    // Piezas fuera de lugar
    public static int calcularFueraDeLugar(String estado, String objetivo) {
        int cont = 0;
        String[] actual = estado.split(",");
        String[] obj = objetivo.split(",");
        for (int i = 0; i < 25; i++) {
            if (!actual[i].equals("0") && !actual[i].equals(obj[i])) cont++;
        }
        return cont;
    }
}