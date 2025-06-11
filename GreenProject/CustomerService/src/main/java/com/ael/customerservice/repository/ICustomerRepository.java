package com.ael.customerservice.repository;

import com.ael.customerservice.dto.response.AddressResponse;
import com.ael.customerservice.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ICustomerRepository extends JpaRepository<Customer, Integer> {
    Optional<Customer> findCustomerByUserNameOrEmail(String email, String userName);
    Optional<Customer> findCustomerByUserNameOrPassword(String username,String password);
    Optional<Boolean> existsByEmailOrUserName(String email, String userName);
}
