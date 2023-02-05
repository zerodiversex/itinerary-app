package fr.sorbonneuniversity.csamicroservice.entities;

import jakarta.persistence.Column;
import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "transfer")
public class Transfer {
    @EmbeddedId
    private TransferId transferId;

    @Column(name = "min_transfer_time")
    private Long minTransferTime;
}
