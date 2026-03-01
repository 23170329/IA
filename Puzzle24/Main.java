import java.util.LinkedList;
import java.util.List;
import java.util.ArrayList;

public class Main {
    static class Resultado {
        String nombre;
        long nodos;
        long tiempo;
        int movimientos;

        Resultado(String n, long nod, long t, int m) {
            this.nombre = n;
            this.nodos = nod;
            this.tiempo = t;
            this.movimientos = m;
        }
    }

    public static void main(String[] args) {
        String inicial = "1,2,0,3,5,6,7,8,4,9,11,12,14,15,10,16,17,13,18,19,21,22,23,24,20";
        String objetivo = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0";

        List<Resultado> comparativa = new ArrayList<>();

        System.out.println("Iniciando búsqueda...");

        // Manhattan
        System.out.println("\n--- Manhattan ---");
        Resultado resManhattan = ejecutarYObtener(inicial, objetivo, true, "Manhattan");
        if (resManhattan != null) {
            comparativa.add(resManhattan);
            System.out.println("Solución encontrada.");
        }

        // Fuera de Lugar
        System.out.println("\n--- Fuera de Lugar ---");
        Resultado resFuera = ejecutarYObtener(inicial, objetivo, false, "Fuera de Lugar");
        if (resFuera != null) {
            comparativa.add(resFuera);
            System.out.println("Solución encontrada.");
        }

        System.out.println("\n\n=== ANALISIS ===");
        System.out.printf("%-20s | %-12s | %-12s | %-5s%n", "Heuristica", "Nodos Exp.", "Tiempo (ms)", "Movs");
        System.out.println("-----------------------------------------------------------------------");

        for (Resultado r : comparativa) {
            System.out.printf("%-20s | %-12d | %-12d | %-5d%n",
                    r.nombre, r.nodos, r.tiempo, r.movimientos);
        }
    }

    private static Resultado ejecutarYObtener(String ini, String obj, boolean m, String nombre) {
        Nodo raiz = new Nodo(ini);
        ArbolDeBusqueda buscador = new ArbolDeBusqueda(raiz);

        long tInicio = System.currentTimeMillis();
        Nodo solucion = buscador.buscarIDAStar(obj, m);
        long tFin = System.currentTimeMillis();

        if (solucion != null) {
            if (m) {
                imprimirCamino(reconstruirCamino(solucion));
            }
            return new Resultado(nombre, buscador.getNodosExpandidos(), (tFin - tInicio), solucion.getNivel());
        }
        return null;
    }
    private static List<String> reconstruirCamino(Nodo nodo) {
        LinkedList<String> camino = new LinkedList<>();
        while (nodo != null) {
            camino.addFirst(nodo.getEstado());
            nodo = nodo.getPadre();
        }
        return camino;
    }

    private static void imprimirCamino(List<String> camino) {
        for (String estado : camino) {
            imprimirTablero(estado);
            System.out.println("-----------");
        }
    }

    private static void imprimirTablero(String e) {
        String[] p = e.split(",");
        for (int i = 0; i < 25; i++) {
            System.out.print(p[i] + "\t");
            if ((i + 1) % 5 == 0) System.out.println();
        }
    }
}