import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Set;

public class ArbolDeBusqueda {

    private Nodo raiz;

    public ArbolDeBusqueda(Nodo raiz) {
        this.raiz = raiz;
    }

    // BUSQUEDA EN ANCHURA (BFS)
    public Nodo buscarBFS(String objetivo) {
        if (raiz == null)
            return null;

        Set<String> visitados = new HashSet<>();
        Queue<Nodo> cola = new LinkedList<>();

        cola.add(raiz);
        visitados.add(raiz.getEstado());

        while (!cola.isEmpty()) {
            Nodo actual = cola.poll();

            if (actual.getEstado().equals(objetivo)) {
                return actual;
            }

            for (Nodo hijo : actual.generarSucesores()) {
                if (!visitados.contains(hijo.getEstado())) {
                    visitados.add(hijo.getEstado());
                    cola.add(hijo);
                }
            }
        }
        return null;
    }

    // BUSQUEDA EN PROFUNDIDAD (DFS)
    public Nodo buscarDFS(String objetivo) {
        if (raiz == null)
            return null;

        Set<String> visitados = new HashSet<>();
        Deque<Nodo> pila = new ArrayDeque<>();

        pila.push(raiz);
        visitados.add(raiz.getEstado());

        while (!pila.isEmpty()) {
            Nodo actual = pila.pop();

            if (actual.getEstado().equals(objetivo)) {
                return actual;
            }

            List<Nodo> hijos = actual.generarSucesores();

            for (int i = hijos.size() - 1; i >= 0; i--) {
                Nodo hijo = hijos.get(i);
                if (!visitados.contains(hijo.getEstado())) {
                    visitados.add(hijo.getEstado());
                    pila.push(hijo);
                }
            }
        }
        return null;
    }

    // BUSQUEDA DE COSTO UNIFORME
    public Nodo buscarCostoUniforme(String objetivo) {
        if (raiz == null)
            return null;

        Set<String> visitados = new HashSet<>();
        Queue<Nodo> cola = new LinkedList<>();

        cola.add(raiz);
        visitados.add(raiz.getEstado());

        // posiciones que evaluamos (heurística)
        int[] posiciones = { 0, 2, 4, 6, 8 };

        while (!cola.isEmpty()) {
            Nodo actual = cola.poll();

            if (actual.getEstado().equals(objetivo)) {
                return actual;
            }

            List<Nodo> hijos = actual.generarSucesores();
            Nodo mejor = null;
            int mejorScore = -1;

            for (Nodo hijo : hijos) {
                if (visitados.contains(hijo.getEstado()))
                    continue;

                hijo.setPadre(actual);
                hijo.setNivel(actual.getNivel() + 1);

                int score = 0;
                for (int pos : posiciones) {
                    if (hijo.getEstado().charAt(pos) == objetivo.charAt(pos)) {
                        score++;
                    }
                }
                hijo.setCosto(score);

                if (score > mejorScore) {
                    mejor = hijo;
                    mejorScore = score;
                }
            }

            if (mejor != null) {
                visitados.add(mejor.getEstado());
                cola.add(mejor);
            } else {
                for (Nodo hijo : hijos) {
                    if (!visitados.contains(hijo.getEstado())) {
                        hijo.setPadre(actual);
                        hijo.setNivel(actual.getNivel() + 1);
                        visitados.add(hijo.getEstado());
                        cola.add(hijo);
                    }
                }
            }
        }
        return null;
    }
}
