import java.util.LinkedList;
import java.util.List;

public class Main {

    public static void main(String[] args) {

        String estadoInicial = "1238 4765";
        String estadoObjetivo = "1284376 5";

        Nodo raiz = new Nodo(estadoInicial);
        ArbolDeBusqueda buscador = new ArbolDeBusqueda(raiz);

        Nodo solucion = buscador.buscarBFS(estadoObjetivo);

        if (solucion == null) {
            System.out.println("No se encontró solución.");
            return;
        }

        System.out.println("Estado objetivo encontrado:");
        System.out.println(solucion.getEstado());
        System.out.println("Movimientos realizados: " + solucion.getNivel());

        List<String> camino = reconstruirCamino(solucion);
        imprimirCamino(camino);
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
        System.out.println("\nCamino de solución:");

        for (String estado : camino) {
            imprimirTablero(estado);
            System.out.println("-----------");
        }
    }

    private static void imprimirTablero(String e) {
        System.out.println(e.substring(0, 3));
        System.out.println(e.substring(3, 6));
        System.out.println(e.substring(6, 9));
    }
}
