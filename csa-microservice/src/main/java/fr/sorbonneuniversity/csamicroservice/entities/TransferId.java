package fr.sorbonneuniversity.csamicroservice.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Embeddable
public class TransferId implements Serializable {

    @Column(name = "from_stop_id", nullable = false)
    private Long from;
    @Column(name = "to_stop_id", nullable = false)
    private Long to;
}